# roop/core.py

# --- [unchanged imports and setup] ---
from roop.predictor import predict_image, predict_video

# --- inside start() ---
def start() -> None:
    for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):
        if not frame_processor.pre_start():
            return
    # process image to image
    if has_image_extension(roop.globals.target_path):
        # NSFW check disabled
        # if predict_image(roop.globals.target_path):
        #     destroy()
        shutil.copy2(roop.globals.target_path, roop.globals.output_path)

        # process frame
        for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):
            update_status('Progressing...', frame_processor.NAME)
            frame_processor.process_image(roop.globals.source_path, roop.globals.output_path, roop.globals.output_path)
            frame_processor.post_process()

        if is_image(roop.globals.target_path):
            update_status('Processing to image succeed!')
        else:
            update_status('Processing to image failed!')
        return

    # process image to videos
    # NSFW check disabled
    # if predict_video(roop.globals.target_path):
    #     destroy()

    update_status('Creating temporary resources...')
    create_temp(roop.globals.target_path)

    if roop.globals.keep_fps:
        fps = detect_fps(roop.globals.target_path)
        update_status(f'Extracting frames with {fps} FPS...')
        extract_frames(roop.globals.target_path, fps)
    else:
        update_status('Extracting frames with 30 FPS...')
        extract_frames(roop.globals.target_path)

    temp_frame_paths = get_temp_frame_paths(roop.globals.target_path)
    if temp_frame_paths:
        for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):
            update_status('Progressing...', frame_processor.NAME)
            frame_processor.process_video(roop.globals.source_path, temp_frame_paths)
            frame_processor.post_process()
    else:
        update_status('Frames not found...')
        return

    if roop.globals.keep_fps:
        fps = detect_fps(roop.globals.target_path)
        update_status(f'Creating video with {fps} FPS...')
        create_video(roop.globals.target_path, fps)
    else:
        update_status('Creating video with 30 FPS...')
        create_video(roop.globals.target_path)

    if roop.globals.skip_audio:
        move_temp(roop.globals.target_path, roop.globals.output_path)
        update_status('Skipping audio...')
    else:
        if roop.globals.keep_fps:
            update_status('Restoring audio...')
        else:
            update_status('Restoring audio might cause issues as fps are not kept...')
        restore_audio(roop.globals.target_path, roop.globals.output_path)

    update_status('Cleaning temporary resources...')
    clean_temp(roop.globals.target_path)

    if is_video(roop.globals.target_path):
        update_status('Processing to video succeed!')
    else:
        update_status('Processing to video failed!')


def run():
    from roop.ui import start_ui
    start_ui()