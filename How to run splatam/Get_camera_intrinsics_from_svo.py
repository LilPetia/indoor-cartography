import pyzed.sl as sl

zed = sl.Camera()
init_params = sl.InitParameters()
init_params.set_from_svo_file("ZEDCodes/my_output.svo2")  # можно и просто zed.open() если камера подключена
init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # 👈 вместо NEURAL
init_params.svo_real_time_mode = False
zed.open(init_params)

# Получаем параметры камеры
calib = zed.get_camera_information().camera_configuration.calibration_parameters.left_cam

fx = calib.fx
fy = calib.fy
cx = calib.cx
cy = calib.cy

print(f"fx={fx}, fy={fy}, cx={cx}, cy={cy}")
zed.close()

# Сохраним в текстовый файл
with open("camera_intrinsics.txt", "w") as f:
    f.write(f"{fx} {fy} {cx} {cy}\n")
