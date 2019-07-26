# ALS - Astro Live Stacker
# Copyright (C) 2019  Sébastien Durand (Dragonlost) - Gilles Le Maréchal (Gehelem)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Numerical stuff
import numpy as np
import cv2

# Wavelet stuff
import dtcwt
from pywi.processing.transform import starlet

# Local stuff
import stack as stk

name_of_tiff_image = "stack_image.tiff"
name_of_jpeg_image = "stack_image.jpg"


def Wavelets(image, wavelets_type, wavelets_use_luminance, parameters):
    """
    Module allowing to play with coefficients of a redudant frame from the
    wavelet family.
    A ratio is applied to each level
    :param image:      input image
    :param wavelets_type: either 'deep sky' or 'planetary' gives the family
                            of wavelets to be used for processing
    :param parameters: ratio to be applied for each level of the wavelet
                        decomposition
    :return:           denoised/enhanced image
    """

    def apply_dt_wavelets(img, param):
        # Compute 5 levels of dtcwt with the antonini/qshift settings
        input_shape = img.shape
        transform = dtcwt.Transform2d(biort='antonini', qshift='qshift_06')
        t = transform.forward(img, nlevels=len(param))

        for level, ratio in param.items():
            data = t.highpasses[level - 1]
            if ratio < 1:
                norm = np.absolute(data)
                # 1 keeps 100% of the coefficients, 0 keeps 0% of the coeff
                thresh = np.percentile(norm, 100 * (1 - ratio))
                # Proximity operator for L1,2 norm
                data[:, :, :] = np.where(norm < thresh, 0,
                                         (norm - thresh) * np.exp(1j * np.angle(data)))
            else:
                # Just applying gain for this level
                data *= ratio
        ret = transform.inverse(t)
        # in some cases dtcwt does reshape the image for performance purpose
        return ret[:input_shape[0], :input_shape[1]]

    def apply_star_wavelets(img, param):
        # Compute 5 levels of starlets
        t = starlet.wavelet_transform(img, number_of_scales=len(param))

        for level, ratio in param.items():
            data = t[level - 1]
            if ratio < 1:
                norm = np.absolute(data)
                # 1 keeps 100% of the coefficients, 0 keeps 0% of the coeff
                thresh = np.percentile(norm, 100 * (1 - ratio))
                # Proximity operator for L1 norm
                data[:, :] = np.where(norm < thresh, 0,
                                      (norm - thresh) * np.sign(data))
            else:
                # Just applying gain for this level
                data *= ratio
        return starlet.inverse_wavelet_transform(t)

    # Choose in between members of a catalog
    wavelet_db = {'deep sky': apply_star_wavelets,
                  'planetary': apply_dt_wavelets}

    # in case of rgb image with 3 channels
    if len(image.shape) > 2:
        # either process wvlts only on the value channel of hsv space
        if wavelets_use_luminance:
            hsv_img = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            hsv_img[:, :, 2] = wavelet_db[wavelets_type](hsv_img[:, :, 2], parameters)
            image = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)
        # or compute 3 times the wvlt process. More expensive, but usually this
        # yields better results
        else:
            # apply wvlt to all channels if available
            for channel_index in range(image.shape[2]):
                image[:, :, channel_index] = wavelet_db[wavelets_type](
                    image[:, :, channel_index], parameters)
    else:
        image = wavelet_db[wavelets_type](image, parameters)
    return image


def SCNR(rgb_image, im_limit, rgb_type="RGB", scnr_type="ne_m", amount=0.5):
    """
    Function for reduce green noise on image
    SCNR Average Neutral Protection

    :param rgb_image: Numpy array (float32), size 3xMxN
    :param im_type: string, uint16 or uint8
    :param im_limit: int, value limit, 255 or 65535
    :param rgb_type: RGB or BGR
    :param scnr_type: string, correction type : ne_m, ne_max, ma_ad or ma_max
    :param amount: float, 0 to 1, param for ma_ad and ma_max
    :return: image corrected (np.array(float32))

    """

    # Swap blue and red for different mode :
    if rgb_type == "RGB":
        red = 0
        blue = 2
    elif rgb_type == "BGR":
        red = 2
        blue = 0

    # process image
    if scnr_type == "Av Neutral":
        m = (rgb_image[red] + rgb_image[blue]) * 0.5
        compare = rgb_image[1] < m
        rgb_image[1] = compare * rgb_image[1] + np.invert(compare) * m

    elif scnr_type == "Max Neutral":
        compare = rgb_image[red] > rgb_image[blue]
        m = compare * rgb_image[red] + np.invert(compare) * rgb_image[blue]
        compare = rgb_image[1] < m
        rgb_image[1] = compare * rgb_image[1] + np.invert(compare) * m

    elif scnr_type == "Add Mask":
        rgb_image = rgb_image / im_limit
        unity_m = np.ones((rgb_image[1].shape[0], rgb_image[1].shape[1]))
        compare = unity_m < (rgb_image[blue] + rgb_image[red])
        m = compare * unity_m + np.invert(compare) * (rgb_image[blue] + rgb_image[red])
        rgb_image[1] = rgb_image[1] * (1 - amount) * (1 - m) + m * rgb_image[1]
        rgb_image = rgb_image * im_limit

    elif scnr_type == "Max Mask":
        rgb_image = rgb_image / im_limit
        compare = rgb_image[red] > rgb_image[blue]
        m = compare * rgb_image[red] + np.invert(compare) * rgb_image[blue]
        rgb_image[1] = rgb_image[1] * (1 - amount) * (1 - m) + m * rgb_image[1]
        rgb_image = rgb_image * im_limit

    return rgb_image


def save_tiff(work_path, stack_image, log, mode="rgb", scnr_on=False,
              wavelets_on=False, wavelets_type='deep sky',
              wavelets_use_luminance=False, param=[], image_type="tiff"):
    """
    Fonction for create print image and post process this image

    :param work_path: string, path for work folder
    :param stack_image: np.array(uintX), Image, 3xMxN or MxN
    :param log: QT log for print text in QT GUI
    :param mode: image mode ("rgb" or "gray")
    :param scnr_on: bool, activate scnr correction
    :param wavelets_on: bool, activate wavelet filtering
    :param param: post process param
    :param image_type: "tiff", "no" and "jpeg"
    :return: no return

    """

    # change action for mode :
    if mode == "rgb":
        log.append(_("Save New Image in RGB..."))
        # convert clissic classic order to cv2 order
        new_stack_image = np.rollaxis(stack_image, 0, 3)
        # convert RGB color order to BGR
        new_stack_image = cv2.cvtColor(new_stack_image, cv2.COLOR_RGB2BGR)
    elif mode == "gray":
        log.append(_("Save New Image in B&W..."))
        new_stack_image = stack_image

    # read image number type
    limit, im_type = stk.test_utype(new_stack_image)

    # if no have change, no process
    if param[0] != 1 or param[1] != 0 or param[2] != 0 or param[3] != limit \
            or param[4] != 1 or param[5] != 1 or param[6] != 1 or any(
        [v != 1 for _, v in param[9].items()]):

        # print param value for post process
        log.append(_("Post-Process New Image..."))
        log.append(_("correct display image"))
        log.append(_("contrast value :") + " %f" % param[0])
        log.append(_("brightness value :") + "%f" % param[1])
        log.append(_("pente : ") + "%f" % (1. / ((param[3] - param[2]) / limit)))

        # need convert to float32 for excess value
        new_stack_image = np.float32(new_stack_image)

        if scnr_on:
            log.append(_("apply SCNR"))
            log.append(_("SCNR type") + "%s" % param[7])
            new_stack_image = SCNR(new_stack_image, limit, rgb_type="BGR", scnr_type=param[7], amount=param[8])

        if wavelets_on:
            log.append("apply Wavelets")
            log.append("Wavelets parameters {}".format(param[9]))
            new_stack_image = Wavelets(new_stack_image,
                                       wavelets_type=wavelets_type,
                                       wavelets_use_luminance=wavelets_use_luminance,
                                       parameters=param[9])

        # if change in RGB value
        if param[4] != 1 or param[5] != 1 or param[6] != 1:
            if mode == "rgb":
                # invert Red and Blue for cv2
                # print RGB contrast value
                log.append(_("R contrast value : ") + "%f" % param[4])
                log.append(_("G contrast value : ") + "%f" % param[5])
                log.append(_("B contrast value : ") + "%f" % param[6])

                # multiply by RGB factor
                new_stack_image[:, :, 0] = new_stack_image[:, :, 0] * param[6]
                new_stack_image[:, :, 1] = new_stack_image[:, :, 1] * param[5]
                new_stack_image[:, :, 2] = new_stack_image[:, :, 2] * param[4]

        # if change in limit value
        if param[2] != 0 or param[3] != limit:
            # filter excess value with new limit
            new_stack_image = np.where(new_stack_image < param[3], new_stack_image, param[3])
            new_stack_image = np.where(new_stack_image > param[2], new_stack_image, param[2])
            # spread out the remaining values
            new_stack_image = new_stack_image * (1. / ((param[3] - param[2]) / limit))

        # if chage in contrast/brightness value
        if param[0] != 1 or param[1] != 0:
            # new_image = image * contrast + brightness
            new_stack_image = new_stack_image * param[0] + param[1]

        # filter excess value > limit
        new_stack_image = np.where(new_stack_image < limit, new_stack_image, limit)
        new_stack_image = np.where(new_stack_image > 0, new_stack_image, 0)

        # reconvert in unintX format
        if im_type == "uint16":
            new_stack_image = np.uint16(new_stack_image)
        elif im_type == "uint8":
            new_stack_image = np.uint8(new_stack_image)

    # use cv2 fonction for save print image in tiff format
    if image_type == "tiff":
        cv2.imwrite(work_path + "/" + name_of_tiff_image, new_stack_image)
        print(_("TIFF image create :") + "%s" % work_path + "/" + name_of_tiff_image)
        new_stack_image = cv2.cvtColor(new_stack_image, cv2.COLOR_BGR2RGB)
    elif image_type == "jpeg":
        cv2.imwrite(work_path + "/" + name_of_jpeg_image, new_stack_image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        print(_("JPEG image create :") + "%s" % work_path + "/" + name_of_jpeg_image)
        new_stack_image = cv2.cvtColor(new_stack_image, cv2.COLOR_BGR2RGB)
    elif image_type == "no":
        print(_("No image create, als use RAM"))
        new_stack_image = cv2.cvtColor(new_stack_image, cv2.COLOR_BGR2RGB)
    return new_stack_image
