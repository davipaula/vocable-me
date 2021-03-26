def _format_time(time_str: str) -> str:
    return time_str.split(".")[0].replace(":", "_")


def _clean_text(text):
    # TODO clean text in the dataset ingestion
    return text.replace("\n", " ")


def _format_file_name(start_time: str, end_time: str, title: str):
    start = _format_time(start_time)
    end = _format_time(end_time)

    return f"{start}-{end}-{title}.mp3"


class VideoCaption:
    def __init__(self, title: str, text: str, start_time: str, end_time: str):
        self.video_id = title
        self.title = self.video_id.split(".")[0]
        self.text = _clean_text(text)
        self.start_time = start_time
        self.end_time = end_time

    def get_original_filename(self):
        return self.title + ".mp3"

    def get_output_filename(self):
        start = _format_time(self.start_time)
        end = _format_time(self.end_time)

        return f"{start}-{end}-{self.title}.mp3"
