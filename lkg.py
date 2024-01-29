import os
import shutil
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QPushButton, QTextEdit

class FileMover(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.source_folder = None
        self.destination_folder = None

        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        source_button = QPushButton('소스 폴더 선택')
        source_button.clicked.connect(self.select_source_folder)
        layout.addWidget(source_button)

        destination_button = QPushButton('대상 폴더 선택')
        destination_button.clicked.connect(self.select_destination_folder)
        layout.addWidget(destination_button)

        move_button = QPushButton('파일 이동')
        move_button.clicked.connect(self.move_files)
        layout.addWidget(move_button)

        self.setLayout(layout)
        self.setWindowTitle('파일 이동 프로그램')
        self.show()

    def select_source_folder(self):
        self.source_folder = QFileDialog.getExistingDirectory(self, '소스 폴더 선택', '')

    def select_destination_folder(self):
        self.destination_folder = QFileDialog.getExistingDirectory(self, '대상 폴더 선택', '')

    def move_files(self):
        try:
            if not self.source_folder or not self.destination_folder:
                print("소스 폴더와 대상 폴더를 선택하세요.")
                return

            # 텍스트 에디터에서 파일 이름들을 읽어옵니다.
            file_names = [line.strip() for line in self.text_edit.toPlainText().split('\n') if line.strip()]

            for file_name in file_names:
                source_path = os.path.join(self.source_folder, file_name)
                destination_path = os.path.join(self.destination_folder, file_name)

                if os.path.exists(source_path):
                    # 파일을 이동하고, 원본 파일을 삭제합니다.
                    shutil.move(source_path, destination_path)
                    print(f"{file_name} 파일을 이동했습니다.")
                else:
                    print(f"{file_name} 파일이 소스 폴더에 존재하지 않습니다.")

        except Exception as e:
            print("오류 발생:", str(e))


def main():
    app = QApplication([])
    mover = FileMover()
    app.exec_()


if __name__ == "__main__":
    main()
