import tkinter as tk

from scipy.signal import wiener


class App(tk.Tk):
    def __init__(self, *args):
        super().__init__()
        self.title("Inventory Management")
        self.height = 500
        self.width = 1000
        # self.geometry(f"{self.width}x{self.height}")
        self.minsize(self.width, self.height)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.pages= args

        self.frames = {}

        for F in self.pages:
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        #create a canvas
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="news")

        self.canvas.create_oval(-200, -100, 700, 700, fill="red", outline="black")

        # tk.Label(self, text="Login Page").pack(pady=10)
        # tk.Button(self, text="Go to Register",
        #           command=lambda: controller.show_frame("RegisterPage")).pack()
        # tk.Button(self, text="Forgot Password?",
        #           command=lambda: controller.show_frame("ResetPasswordPage")).pack()

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Register Page").pack(pady=10)
        tk.Button(self, text="Back to Login",
                  command=lambda: controller.show_frame("LoginPage")).pack()

class ResetPasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Reset Password Page").pack(pady=10)
        tk.Button(self, text="Back to Login",
                  command=lambda: controller.show_frame("LoginPage")).pack()

if __name__ == "__main__":
    app = App(LoginPage, RegisterPage, ResetPasswordPage)
    app.mainloop()
