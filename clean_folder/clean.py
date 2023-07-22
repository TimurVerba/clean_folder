import argparse
from pathlib import Path
import shutil
import sys
import re



"""normalize"""

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r"\W", ".", t_name)
    return t_name


"""file_parser"""

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
AVI_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
MP4_VIDEO = []
DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
MP3_AUDIO = []
MY_OTHER = []
ZIP_ARCHIVES = []
TAR_ARCHIVES = []
GZ_ARCHIVES = []

REGISTER_EXTENSION = {
    "JPEG": JPEG_IMAGES,
    "JPG": JPG_IMAGES,
    "PNG": PNG_IMAGES,
    "SVG": SVG_IMAGES,
    "AVI": AVI_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    "MP4": MP4_VIDEO,
    "DOC": DOC_DOCUMENTS,
    "DOCX": DOCX_DOCUMENTS,
    "TXT": TXT_DOCUMENTS,
    "PDF": PDF_DOCUMENTS,
    "XLSX": XLSX_DOCUMENTS,
    "PPTX": PPTX_DOCUMENTS,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    "MP3": MP3_AUDIO,
    "ZIP": ZIP_ARCHIVES,
    "GZ": GZ_ARCHIVES,
    "TAR": TAR_ARCHIVES,

}

FOLDERS = []
EXTENSION = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ("ARCHIVES", "videos", "audio", "documents", "images", "MY_OTHER"):
                FOLDERS.append(item)
                scan(item)
            continue
        ext = get_extension(item.name)
        fullname = folder / item.name
        if not ext:
            MY_OTHER.append(fullname)
        else:
            try:
                container = REGISTER_EXTENSION[ext]
                EXTENSION.add(ext)
                container.append(fullname)
            except KeyError:
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)


def handle_media(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path) -> None:
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ""))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    if filename.exists():
        try:
            shutil.unpack_archive(filename, folder_for_file)
        except shutil.ReadError:
            print("It is not an archive")
            folder_for_file.rmdir()
        if any(folder_for_file.iterdir()):
            filename.unlink()
        else:
            print(f"Не удалось распаковать архив {filename}")
    else:
        print(f"Файл {filename} не найден")


def handler_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f"Can`t delete folder: {folder}")

def main(folder: Path):
    scan(folder)
    for file in JPEG_IMAGES:
        handle_media(file, folder / "images" / "JPEG")
    for file in JPG_IMAGES:
        handle_media(file, folder / "images" / "JPG")
    for file in PNG_IMAGES:
        handle_media(file, folder / "images" / "PNG")
    for file in SVG_IMAGES:
        handle_media(file, folder / "images" / "SVG")

    for file in AVI_VIDEO:
        handle_media(file, folder / "videos" / "AVI")
    for file in MP4_VIDEO:
        handle_media(file, folder / "videos" / "MP4")
    for file in MOV_VIDEO:
        handle_media(file, folder / "videos" / "MOV")
    for file in MKV_VIDEO:
        handle_media(file, folder / "videos" / "MKV")

    for file in OGG_AUDIO:
        handle_media(file, folder / "audio" / "OGG")
    for file in WAV_AUDIO:
        handle_media(file, folder / "audio" / "WAV")
    for file in AMR_AUDIO:
        handle_media(file, folder / "audio" / "AMR")
    for file in MP3_AUDIO:
        handle_media(file, folder / "audio" / "MP3")

    for file in DOC_DOCUMENTS:
        handle_media(file, folder / "documents" / "DOC")
    for file in DOCX_DOCUMENTS:
        handle_media(file, folder / "documents" / "DOCX")
    for file in TXT_DOCUMENTS:
        handle_media(file, folder / "documents" / "TXT")
    for file in PDF_DOCUMENTS:
        handle_media(file, folder / "documents" / "PDF")
    for file in XLSX_DOCUMENTS:
        handle_media(file, folder / "documents" / "XLSX")
    for file in PPTX_DOCUMENTS:
        handle_media(file, folder / "documents" / "PPTX")



    for file in MY_OTHER:
        handle_other(file, folder / "MY_OTHER")
    for file in ZIP_ARCHIVES:
        handle_archive(file, folder / "ARCHIVES" / "ZIP")
    for file in GZ_ARCHIVES:
        handle_archive(file, folder / "ARCHIVES" / "GZ")
    for file in TAR_ARCHIVES:
        handle_archive(file, folder / "ARCHIVES" / "TAR")

    for folder in FOLDERS[::-1]:
        handler_folder(folder)

def run():
    if sys.argv[1]:
        folder_for_scan = Path(sys.argv[1])
        print(f"Start in folder: {folder_for_scan.resolve()}")
        main(folder_for_scan.resolve())
        print(f"Images jpeg: {JPEG_IMAGES}")
        print(f"Images jpg: {JPG_IMAGES}")
        print(f"Images svg: {SVG_IMAGES}")
        print(f"Images png: {PNG_IMAGES}")
        print(f"Audio mp3: {MP3_AUDIO}")
        print(f"Audio amr: {AMR_AUDIO}")
        print(f"Audio ogg: {OGG_AUDIO}")
        print(f"Audio wav: {WAV_AUDIO}")
        print(f"Video mp4: {MP4_VIDEO}")
        print(f"Video mkv: {MKV_VIDEO}")
        print(f"Video mov: {MOV_VIDEO}")
        print(f"Video avi: {AVI_VIDEO}")
        print(f"Documents doc: {DOC_DOCUMENTS}")
        print(f"Documents docx: {DOCX_DOCUMENTS}")
        print(f"Documents txt: {TXT_DOCUMENTS}")
        print(f"Documents pdf: {PDF_DOCUMENTS}")
        print(f"Documents xlsx: {XLSX_DOCUMENTS}")
        print(f"Documents pptx: {PPTX_DOCUMENTS}")

        print(f"Archives_ZIP: {ZIP_ARCHIVES}")
        print(f"Archives_GZ: {GZ_ARCHIVES}")
        print(f"Archives_TAR: {TAR_ARCHIVES}")

        print(f"Types of file in folder: {EXTENSION}")
        print(f"Unknown files of types: {UNKNOWN}")
        print(f"MY_OTHER: {MY_OTHER}")

        print(FOLDERS[::-1])



if __name__ == "__main__":
    run()

