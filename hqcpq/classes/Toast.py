from windows_toasts import WindowsToaster, ToastText4


class Toast:
    def __init__(self, title: str, body: str):

        self.toast = ToastText4()
        self.toast.SetHeadline(title)
        self.toast.SetBody(body)

    def show(self):

        wintoaster = WindowsToaster("Python")
        wintoaster.show_toast(self.toast)
