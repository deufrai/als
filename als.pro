SOURCES += src/als/main.py \
  src/als/logic.py \
  src/als/stack.py \
  src/als/code_utilities.py \
  src/als/crunching.py \
  src/als/config.py \
  src/als/processing.py \
  src/als/model/data.py \
  src/als/model/base.py \
  src/als/model/params.py \
  src/als/streams/network.py \
  src/als/streams/input.py \
  src/als/streams/output.py \
  src/als/ui/params_utils.py \
  src/als/ui/widgets.py \
  src/als/ui/windows.py \
  src/als/ui/dialogs.py

TRANSLATIONS = i18n/als_fr.ts \
  i18n/als_ru.ts

FORMS += src/als/ui/about_ui.ui \
  src/als/ui/als_ui.ui \
  src/als/ui/save_wait_ui.ui \
  src/als/ui/prefs_ui.ui \
  src/als/ui/stop_ui.ui
