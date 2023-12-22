import json
from pathlib import Path

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton

from source.survey.base import BaseSurvey
from source.survey import Empty, survey_get


class FrameSurvey(QFrame):
    signal_success = pyqtSignal()

    def __init__(self, survey_path: Path | str):
        super().__init__()

        # signals
        self.signal_success.connect(self._on_signal_success)  # NOQA: connect exist

        # prepare the survey screen data
        self.survey_screens: list[tuple[str, BaseSurvey]] = []
        self.current_survey_index = 0

        # prepare the survey collected data
        self.collected_datas: dict[str, dict] = {}

        # set the layout
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        # prepare the frame for the survey elements
        self.frame_survey: BaseSurvey = Empty()
        self._layout.addWidget(self.frame_survey)

        # navigations actions
        self.frame_navigation = QFrame()
        self._layout.addWidget(self.frame_navigation)

        self._layout_navigation = QHBoxLayout()
        self.frame_navigation.setLayout(self._layout_navigation)

        self._layout_navigation.addStretch(0)

        self.button_forward = QPushButton()
        self._layout_navigation.addWidget(self.button_forward)
        self.button_forward.setText("Suivant")
        self.button_forward.clicked.connect(self.next_survey)  # NOQA: connect exist

        # load the survey configuration file
        self.load_file(survey_path)

        # finalize the initialisation
        self.update_survey()

    def _on_signal_success(self):
        # on success, show the button to go forward
        self.button_forward.show()

    def load_file(self, survey_path: Path | str):
        # load the surveys screens
        with open(survey_path, encoding="utf-8") as file:
            surveys_data = json.load(file)

        self.survey_screens = [
            (
                survey_id,
                survey_get(
                    survey_data,
                    signals={"success": self.signal_success}
                )
            )
            for survey_id, survey_data in surveys_data.items()
        ]
        self.current_survey_index = 0

    def next_survey(self):
        # get the collected data from the survey
        collected_data = self.frame_survey.get_collected_data()
        if collected_data is not None:
            # if there is data, get the current survey id
            survey_id, survey = self.survey_screens[self.current_survey_index]
            # save the response in the data
            self.collected_datas[survey_id] = collected_data

            print(collected_data)

        self.current_survey_index += 1

        if self.current_survey_index < len(self.survey_screens):
            self.update_survey()
        else:
            self.finish_survey()

    def update_survey(self):
        # disable the forward button
        self.button_forward.hide()

        # mark the actual survey as the old one
        old_frame_survey = self.frame_survey
        # call the old survey event
        old_frame_survey.on_hide()
        # get the currently selected survey
        survey_id, survey = self.survey_screens[self.current_survey_index]
        # update it to the new one
        self.frame_survey = survey
        # change the widget on the layout
        self._layout.replaceWidget(old_frame_survey, self.frame_survey)
        # call the new survey event
        survey.on_show()
        # delete the old frame
        old_frame_survey.deleteLater()

    def finish_survey(self):
        # TODO: send the collected data as a file somewhere
        print(self.collected_datas)

        self.window().close()
