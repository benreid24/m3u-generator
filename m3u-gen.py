import os
import argparse
import urllib.parse


def path_to_file_uri(path):
    """Convert absolute path to file URI."""
    return urllib.parse.quote(path)


def create_m3u_playlist(input_dir, output_dir, rel_dir, prefix, uri_encode):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    child_folders = [folder for folder in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, folder))]

    for folder in child_folders:
        folder_path = os.path.join(input_dir, folder)
        m3u_path = os.path.join(output_dir, f"{folder.replace(' ', '_')}.m3u8")

        music_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac', '.opus', '.m4a'))]

        with open(m3u_path, 'w', encoding='utf-8') as m3u_file:
            for music_file in music_files:
                full_music_path = os.path.join(folder_path, music_file)
                rel_path = os.path.relpath(full_music_path, rel_dir)
                if uri_encode:
                    rel_path = path_to_file_uri(rel_path)
                m3u_file.write(f'{prefix}{rel_path}\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate M3U playlists for each first level child folder in the parent directory")
    parser.add_argument("-i", "--input_directory", help="Path to the top-level input directory")
    parser.add_argument("-o", "--output_directory", help="Path to the output directory for M3U playlists")
    parser.add_argument("-r", "--relative_to", default="", help="Path to compute relative paths from. Defaults to output_directory")
    parser.add_argument("-p", "--prefix", default="", help="Optional prefix to apply to file paths in the output m3u")
    parser.add_argument("-e", "--uri_encode", default=False, help="Whether to URI encode the output paths or not")
    args = parser.parse_args()

    rp = args.relative_to if args.relative_to else args.output_directory
    create_m3u_playlist(args.input_directory, args.output_directory, rp, args.prefix, args.uri_encode)

