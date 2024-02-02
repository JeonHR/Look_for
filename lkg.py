import os
import shutil
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QPushButton, QTextEdit, QListWidget, QLineEdit, QHBoxLayout

class FileMover(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.source_folder = None
        self.destination_folder = None

        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_edit = QLineEdit()
        search_layout.addWidget(self.search_edit)
        search_button = QPushButton('조회')
        search_button.clicked.connect(self.search_and_display_files)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        source_button = QPushButton('소스 폴더 선택')
        source_button.clicked.connect(self.select_source_folder)
        layout.addWidget(source_button)

        destination_button = QPushButton('대상 폴더 선택')
        destination_button.clicked.connect(self.select_destination_folder)
        layout.addWidget(destination_button)

        self.file_list_widget = QListWidget()
        self.file_list_widget.setSelectionMode(QListWidget.MultiSelection)  # 다중 선택 가능한 code
        layout.addWidget(self.file_list_widget)

        move_button = QPushButton('선택한 파일 이동')
        move_button.clicked.connect(self.move_selected_file)
        layout.addWidget(move_button)

        self.setLayout(layout)
        self.setWindowTitle('파일 이동 프로그램')
        self.show()

    def select_source_folder(self):
        self.source_folder = QFileDialog.getExistingDirectory(self, '소스 폴더 선택', '')

    def select_destination_folder(self):
        self.destination_folder = QFileDialog.getExistingDirectory(self, '대상 폴더 선택', '')

    def search_and_display_files(self):
        try:
            if not self.source_folder:
                print("소스 폴더를 선택하세요.")
                return

            # 텍스트 에디터에서 검색할 텍스트를 읽어옵니다.
            search_text = self.search_edit.text().strip()

            # 검색 결과를 보여주기 전에 기존 목록을 초기화합니다.
            self.file_list_widget.clear()

            # 소스 폴더에서 파일을 찾아 검색 텍스트를 포함하는 경우 목록에 추가합니다.
            for file_name in os.listdir(self.source_folder):
                if search_text in file_name:
                    self.file_list_widget.addItem(file_name)

        except Exception as e:
            print("오류 발생:", str(e))

    def move_selected_file(self):
        try:
            if not self.source_folder or not self.destination_folder:
                print("소스 폴더와 대상 폴더를 선택하세요.")
                return

            # 사용자가 선택한 파일 이름을 가져옵니다.
            selected_item = self.file_list_widget.currentItem()

            if selected_item:
                file_name = selected_item.text()
                source_path = os.path.join(self.source_folder, file_name)
                destination_path = os.path.join(self.destination_folder, file_name)

                if os.path.exists(source_path):
                    # 파일을 이동하고, 원본 파일을 삭제합니다.
                    shutil.move(source_path, destination_path)
                    print(f"{file_name} 파일을 이동했습니다.")
                    # 파일 이동 후 목록을 갱신합니다.
                    self.search_and_display_files()
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
