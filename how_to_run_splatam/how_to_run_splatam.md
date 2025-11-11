# Введение

Здесь я опишу, как запустить splatam для реконструкции 3d сцены из гауссиан по видео формата .svo2. Я запускал всё на windows, но для ubuntu всё тоже должно работать. Для запуска по этой инструкции необходима anaconda и установленный ZED SDK.

## Установка

Сначала надо установить splatam.
Для этого нужно клонировать репозиторий https://github.com/spla-tam/SplaTAM.git в любую удобную папку. Затем необходимо открыть командную строку anaconda в этой папке.
В открытой командной строке выполнить инструкции по установке для anaconda, указанные в репозитории в Readme. После этого splatam будет установлен.

Затем необходимо установить Open3d. Я устанавливал его в ту же среду anaconda, что и splatam. Чтобы установить Open3d с поддержкой cuda необходимо собрать его из исходников.
Для этого нужно клонировать репозиторий https://github.com/isl-org/Open3D в любую удобную папку.
Затем для Windows необходимо изменить CMakeLists.txt, находящийся в основной папке клонированного репозитория, нужно ли это делать в Ubuntu я не знаю, в CMakeLists.txt необходимо добавить строку set(CMAKE_CUDA_FLAGS "--diag-suppress 221" CACHE STRING "Additional flags for nvcc" FORCE) после
```
# Build CUDA module by default if CUDA is available
if(BUILD_CUDA_MODULE)
До правки фрагмент кода выглядит так:
...
# Build CUDA module by default if CUDA is available
if(BUILD_CUDA_MODULE)
    if(MSVC)
        # Handle/suppress nvcc unsupported compiler error for MSVC>=1940 with CUDA 11.7 to 12.4:
        # (https://forums.developer.nvidia.com/t/problems-with-latest-vs2022-update/294150/12)
        # Find CUDAToolkit first to get CUDAToolkit_VERSION:
        find_package(CUDAToolkit REQUIRED)
        if (CUDAToolkit_VERSION VERSION_LESS "12.5" AND MSVC_VERSION GREATER_EQUAL 1940)
            # Set required nvcc flags before enable_language(CUDA).
            # Note: CMake >=3.29.4 might be needed for CMAKE_CUDA_FLAGS to be passed correctly to
            # CMake's try_compile environment.
            set(CMAKE_CUDA_FLAGS
                  "${CMAKE_CUDA_FLAGS} -allow-unsupported-compiler -D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH"
                  CACHE STRING "Flags for NVCC" FORCE)
            message(WARNING "Using --allow-unsupported-compiler flag and -D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH for nvcc<=12.4 with MSVC>=1940. "
            "Set $Env:NVCC_PREPEND_FLAGS='--allow-unsupported-compiler' if nvcc still fails.")
        endif()
    endif()
    ...
```
После правки:
```
...
# Build CUDA module by default if CUDA is available
if(BUILD_CUDA_MODULE)
    set(CMAKE_CUDA_FLAGS "--diag-suppress 221" CACHE STRING "Additional flags for nvcc" FORCE)
    if(MSVC)
        # Handle/suppress nvcc unsupported compiler error for MSVC>=1940 with CUDA 11.7 to 12.4:
        # (https://forums.developer.nvidia.com/t/problems-with-latest-vs2022-update/294150/12)
        # Find CUDAToolkit first to get CUDAToolkit_VERSION:
        find_package(CUDAToolkit REQUIRED)
        if (CUDAToolkit_VERSION VERSION_LESS "12.5" AND MSVC_VERSION GREATER_EQUAL 1940)
            # Set required nvcc flags before enable_language(CUDA).
            # Note: CMake >=3.29.4 might be needed for CMAKE_CUDA_FLAGS to be passed correctly to
            # CMake's try_compile environment.
            set(CMAKE_CUDA_FLAGS
                  "${CMAKE_CUDA_FLAGS} -allow-unsupported-compiler -D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH"
                  CACHE STRING "Flags for NVCC" FORCE)
            message(WARNING "Using --allow-unsupported-compiler flag and -D_ALLOW_COMPILER_AND_STL_VERSION_MISMATCH for nvcc<=12.4 with MSVC>=1940. "
            "Set $Env:NVCC_PREPEND_FLAGS='--allow-unsupported-compiler' if nvcc still fails.")
        endif()
    endif()
    ...
```
Без этого установка не будет закончена из-за ошибок.
Затем открыть командную строку anaconda в папке клонированного репозитория и активировать среду выполнения: conda activate splatam.
Затем выполнить инструкции, указанные на сайте https://www.open3d.org/docs/latest/compilation.html, для Windows начиная с пункта 2. Config.
После выполнения инструкций Open3d должен быть установлен в запущенном окружении anaconda.

### Подготовка данных

splatam ожидает, что данные будут представлены в виде файлов с изображениями формата .png, карт глубин для каждого изображения в виде файлов формата .png и файла transforms.json, в котором будут указаны некоторые параметры данных.
Для получения нужных данных из видео нужно запустить скрипт get_RGB_D_from_svo.py, указав в нём свой путь до видео и пути к выходным папкам, в выходных папках не должно храниться других изображений формата .png. Затем для получения внутренних параметров камеры нужно запустить скрипт get_camera_intrinsics_from_svo.py, указав свой путь до видео. 
Затем для перевода карт глубин в формат .png из формата .npy нужно запустить скрипт from_npy_to_png.py, указав путь к папке с картами глубин и путь к выходной папке. Чтобы создать файл transforms.json нужно запустить скрипт make_json.py, указав пареметры камеры (параметр camera_angle_x я примерно оценил как 1.771), путь к папке с изображениями, путь к папке с глубинами и изменив
        "file_path": f"rgb/{rgb}",
        "depth_path": f"depth/{depth}",
так, чтобы они показывали относительные пути (по отношению к файлу transforms.json) к папкам с изображениями и глубинами.
Структура папок у меня:
data/
├── rgb/
│   ├── 000001.png
│   ├── 000002.png
├── depth/
│   ├── 000001.png
│   ├── 000002.png
├── transforms.json

#### Запуск splatam

Нужно в файлах splatam найти \configs\iphone\splatam.py и заменить на указанный в этом репозитории, в нём хранятся настройки для выполнения скрипта splatam.
В basedir необходимо указать свой путь до transforms.json
```
data=dict(
    ...
    basedir=#your path to transforms.json
    ...
)
```
В workdir необходимо указать папку, куда будет записан вывод программы.
Например, basedir='C:/Users/Admin/Documents/ZEDCodes/data',
workdir = 'C:/Users/Admin/Documents/SplaTAM/experiments/ZED_reconstruction'
Затем в этом файле можно изменить некоторые параметры.
Для запуска splatam необходимо в настроенном ранее окружении anaconda из папки, содержащей скачанный splatam выполнить python scripts/splatam.py configs/iphone/splatam.py
После работы программы в выходной папке появится файл params.npz с параметрами полученных гауссианов.

##### Визуализация

Можно изменить параметры визуализации в файле \configs\iphone\splatam_viz.py, а также в этом файле в scene_path неоходимо указать путь до params.npz
```
config = dict(
    scene_path= #your path to params.npz
    ...
)
```
Например, scene_path='C:/Users/Admin/Documents/SplaTAM/experiments/ZED_reconstruction/SplaTAM_iPhone/params.npz'.
Затем нужно запустить визуализацию командой python viz_scripts/final_recon.py configs/iphone/splatam_viz.py
При успешном запуске откроется окно Open3D, в котором отобразятся гауссианы.
