import os
import shutil
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout, QPushButton, QTextEdit, QListWidget, QLineEdit, QHBoxLayout, QSizePolicy, QListWidgetItem,  QMessageBox

#### Made by HR
class FileMover(QWidget):
    def __init__(self):
        super().__init__() ## 상속

        self.init_ui() ## UI load

    def init_ui(self):
        self.source_folder = None ## clear 
        self.destination_folder = None ## clear

        layout = QVBoxLayout() ## 수직으로 시작

        search_layout = QHBoxLayout() ## 수평으로 넣기
        self.search_edit = QTextEdit() ## 수평으로 txt file 넣기 QLineEdit-> 한 줄
        self.search_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.search_edit.setMinimumSize(100, 100)
        search_layout.addWidget(self.search_edit) ## 수평 첫 추가
        search_button = QPushButton('조회') ## click 버튼
        search_button.clicked.connect(self.search_and_display_files) ## signal 신호
        search_layout.addWidget(search_button) ## txt 박스에 넣기
        layout.addLayout(search_layout) ## 수직 박스에 추가

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

        copy_button = QPushButton('선택한 파일 복사')
        copy_button.clicked.connect(self.copy_selected_file)
        layout.addWidget(copy_button)

        self.setLayout(layout)
        self.setWindowTitle('파일 이동 및 복사 프로그램')
        self.show()  ### 앱을 실행하는 기능

    def select_source_folder(self): ### 클릭 시 반응하는 기능
        self.source_folder = QFileDialog.getExistingDirectory(self, '소스 폴더 선택', '')

    def select_destination_folder(self): ### 클릭 시 반응하는 기능
        self.destination_folder = QFileDialog.getExistingDirectory(self, '대상 폴더 선택', '')

    def search_and_display_files(self): ### 클릭 시 반응하는 기능
        try:
            if not self.source_folder: # not 아니면 실행 X
                QMessageBox.warning(self, 'Error','소스 폴더를 선택하세요.', QMessageBox.Ok)
                print("소스 폴더를 선택하세요.")
                return

            # 텍스트 에디터에서 검색할 텍스트를 읽어옵니다.
            search_texts = self.search_edit.toPlainText().strip().split('\n') ## 여기서 각 list로 만드는 의미
            

            # 검색 결과를 보여주기 전에 기존 목록을 초기화합니다.
            self.file_list_widget.clear()
            
            found_files = [file_name for file_name in os.listdir(self.source_folder) if any(substring in file_name for substring in search_texts)]

            if not found_files:
                QMessageBox.warning(self, '알림', '검색 결과가 없습니다.', QMessageBox.Ok)
                return

            for file_name in found_files:
                item = QListWidgetItem(file_name)
                self.file_list_widget.addItem(item)

        except Exception as e:
            print("오류 발생:", str(e))

    def move_selected_file(self):
        try:
            if not self.source_folder or not self.destination_folder:
                print("소스 폴더와 대상 폴더를 선택하세요.")
                QMessageBox.warning(self, 'Error','대상 폴더를 선택하세요.', QMessageBox.Ok) ## 대상 폴더 없을 때 뜨는 Error
                return

            # 사용자가 선택한 파일 이름을 가져옵니다.
            selected_items = [self.file_list_widget.item(i) for i in range(self.file_list_widget.count())]
            selected_files = [item.text() for item in selected_items]

            for file_name in selected_files:
                source_path = os.path.join(self.source_folder, file_name)
                destination_path = os.path.join(self.destination_folder, file_name)

                if os.path.exists(source_path):
                    # 파일을 이동하고, 원본 파일을 삭제합니다. 이동이 복사보다 빠름
                    shutil.move(source_path, destination_path)
                    print(f"{file_name} 파일을 이동했습니다.")
                    # 파일 이동 후 목록을 갱신합니다.  파일 삭제하는 경우에는 중요함
                    self.search_and_display_files()
                else:
                    print(f"{file_name} 파일이 소스 폴더에 존재하지 않습니다.")

        except Exception as e:
            print("오류 발생:", str(e))


    def copy_selected_file(self):
        try:
            if not self.source_folder or not self.destination_folder:
                print("소스 폴더와 대상 폴더를 선택하세요.")
                QMessageBox.warning(self, 'Error','대상 폴더를 선택하세요.', QMessageBox.Ok)
                return

            # 사용자가 선택한 파일 이름을 가져옵니다.
            selected_items = [self.file_list_widget.item(i) for i in range(self.file_list_widget.count())]
            selected_files = [item.text() for item in selected_items]

            for file_name in selected_files:
                source_path = os.path.join(self.source_folder, file_name)
                destination_path = os.path.join(self.destination_folder, file_name)

                if os.path.exists(source_path):
                    # 파일을 이동하고, 원본 파일을 삭제합니다. 복사
                    shutil.copy2(source_path, destination_path)
                    print(f"{file_name} 파일을 복사했습니다.")
                    # 파일 이동 후 목록을 갱신합니다.  파일 삭제하는 경우에는 중요함
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
