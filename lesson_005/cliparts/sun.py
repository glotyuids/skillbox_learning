import simple_draw as sd


def draw_sun(origin, angle=0, ray_length=100, core_radius=50, ray_gap = 10, ray_count=8, ray_width=3):
    angle_step = round(360 / ray_count)
    for next_angle in range(angle, 360 + angle, angle_step):
        ray_start_point = sd.get_vector(origin, next_angle, length=core_radius + ray_gap).end_point
        sd.vector(start=ray_start_point, angle=next_angle, length=ray_length, width=ray_width)
    sd.circle(origin, core_radius, width=0)


if __name__ == "__main__":
    sd.resolution = (900, 900)
    sun_center = sd.get_point(450, 450)

    angle = 0
    sun_radius = 160
    core_radius = 50
    sd.take_background()
    while True:
        sd.start_drawing()
        sd.draw_background()
        angle = (angle + 2) % 360
        if core_radius >= 100:
            sun_size_direction = -1
        elif core_radius <= 50:
            sun_size_direction = 1
        core_radius += 2 * sun_size_direction
        draw_sun(sun_center, angle, core_radius=core_radius, ray_length = sun_radius-core_radius-10)
        sd.finish_drawing()
        sd.sleep(0.016)
        if sd.user_want_exit():
            break

    sd.pause()