import MX64 as mx


class AGV:
    def __init__(self) -> None:
        m1 = mx.MX64(1)
        m2 = mx.MX64(2)
        m3 = mx.MX64(3)
        m4 = mx.MX64(4)
        m5 = mx.MX64(5)
        m6 = mx.MX64(6)

        m6.movingspeed_cw(60)
        m3.movingspeed_cw(40)
        m4.movingspeed_cw(40)
        m5.movingspeed_cw(40)

    def up(self,) -> None:
        self.m3.goal_position(1229)
        self.m4.goal_position(1229)
        self.m5.goal_position(1229)

    def down(self,) -> None:
        # Initial position of the plate
        self.m3.goal_position(2048)
        self.m4.goal_position(2048)
        self.m5.goal_position(2048)

    def tilt_left(self,) -> None:
        self.m3.goal_position(1598)
        self.m3.goal_position(2048)
        self.m3.goal_position(2575)

    def tilt_right(self,) -> None:
        self.m3.goal_position(2575)
        self.m4.goal_position(2048)
        self.m5.goal_position(1598)

    def expand(self,) -> None:
        self.m6.goal_position(480)

    def shrink(self,) -> None:
        self.m6.goal_position(2560)
    