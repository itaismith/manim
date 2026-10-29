from manimlib import *
from manimlib.utils.tex_file_writing import LatexError


class StaleDviDemo(Scene):
    def construct(self):
        good_label = TexText(r'\texttt{Tex("0")}').move_to(UP * 3)
        bad_label = TexText(
            r'\texttt{Tex(r"\textbackslash{}badcommand\{x\}")}'
        ).move_to(DOWN * 0.1)
        good = Tex("0", font_size=100).move_to(UP * 1.7)

        self.play(Write(good_label), Write(good), run_time=1)
        self.wait(0.5)
        self.play(Write(bad_label), run_time=1)

        try:
            result = Tex(r"\badcommand{x}", font_size=100)
        except LatexError as error:
            message = str(error).splitlines()[0]
            if "Undefined control sequence" not in message:
                raise
            result = TexText("LatexError: Undefined control sequence", color=RED)

        result.move_to(DOWN * 1.5)
        self.play(Write(result), run_time=1)
        self.wait(2)
