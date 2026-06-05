# SPDX-FileCopyrightText: 2019-2026 The ALS Authors
# SPDX-License-Identifier: GPL-3.0-or-later

set -e

###########################################################################
#
# compute version number for current tag and/or hash
#
# Only ALS version tags are used as application versions:
#   - stable tags: v1, v1.0, v1.0.0
#   - prerelease tags: v1.0-beta1, v1.0-rc1
#
# Other tags, such as deployment test tags, are ignored for app versioning and
# fall back to the regular development build number.
#
###########################################################################

version_tag_pattern='^v[0-9]+(\.[0-9]+)*(-[0-9A-Za-z][0-9A-Za-z._-]*)?$'
tags=$(git tag --contains HEAD)
version_tags=$(echo "${tags}" | grep -E "${version_tag_pattern}" || true)

if [ -z "${version_tags}" ]
then
  version_tag_count=0
else
  version_tag_count=$(echo "${version_tags}" | wc -l)
fi

if [ ${version_tag_count} -gt 1 ]
then
    echo "More that one version tag exists on HEAD. Cancelling ..."
    exit 1
fi

if [ ${version_tag_count} -eq 1 ]
then
  # in here we are sure the version_tags var only contains one tag, so we can safely assign it to version_tag
  version_tag=${version_tags}
  ALS_VERSION_STRING=${version_tag}
else
  ALS_VERSION_STRING=$(grep version src/als/version.py | cut -d'"' -f2)-$(git rev-parse --short HEAD)
  ALS_VERSION_STRING="${ALS_VERSION_STRING}-bld${CI_PIPELINE_ID}"
fi



###########################################################################
#
# export all variables into .dotenv file
#
###########################################################################
echo "ALS_VERSION_STRING=${ALS_VERSION_STRING}" > .dotenv


###########################################################################
#
# dump created env file
#
###########################################################################
echo '######### env file dump START'
cat .dotenv
echo '######### env file dump END'
