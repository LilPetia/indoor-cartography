import pyzed.sl as sl
import cv2
import numpy as np

# 1️⃣ Инициализация
zed = sl.Camera()

init_params = sl.InitParameters()
init_params.set_from_svo_file("ZEDCodes/my_output.svo2")  # путь к файлу
init_params.svo_real_time_mode = False  # обработка без реального времени
init_params.depth_mode = sl.DEPTH_MODE.ULTRA
init_params.coordinate_units = sl.UNIT.METER

err = zed.open(init_params)
if err != sl.ERROR_CODE.SUCCESS:
    print("Ошибка открытия:", err)
    exit(1)

# 2️⃣ Контейнеры
image = sl.Mat()
depth = sl.Mat()

runtime = sl.RuntimeParameters()

frame_idx = 0
while True:
    if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
        # Извлекаем левое изображение (RGB)
        zed.retrieve_image(image, sl.VIEW.LEFT)
        # Извлекаем глубину
        zed.retrieve_measure(depth, sl.MEASURE.DEPTH)

        rgb = image.get_data()[:, :, :3]
        dmap = depth.get_data()

        # Сохраняем или показываем
        cv2.imshow("RGB", rgb)
        cv2.imshow("Depth", dmap / np.nanmax(dmap))

        # Можно сохранить кадры
        cv2.imwrite(f"data/rgb/rgb_{frame_idx:05d}.png", rgb)
        np.save(f"data/depth/depth_{frame_idx:05d}.npy", dmap)

        frame_idx += 1

    # Останавливаем по клавише
    if cv2.waitKey(1) == 27:
        break

zed.close()
