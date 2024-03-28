from os.path import exists
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QTextEdit,
                             QMenuBar, QMenu, QAction, QMessageBox,
                             QFileDialog, QSlider, QDialog, QLabel, QPushButton, QHBoxLayout, QInputDialog)
from PyQt5.QtGui import QFont, QKeyEvent, QKeySequence, QCloseEvent, QTextCursor
from PyQt5.QtCore import Qt
from sys import argv


class Main(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.is_saved = True
        self.fsize = 20
        self.path = 'new'
        self.initialFilter = 'Text files (*.txt);; MarkDown files (*.md);; Batch files (*.bat);; All (*.*)'
        
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(0,0,0,0)
        
        self.text_area = TextArea(self)
        self.text_area.textChanged.connect(self.areatextChanged)
        self.change_textarea_font('Arial', 20)
        
        self.init_menu()
        self.lay.addWidget(self.text_area)
    
    def change_textarea_font(self, fam: str, size: int):
        self.text_area.setFont(QFont(fam, size))
    
    def init_menu(self):
        self.menu = QMenuBar(self)
        self.init_file_menu()
        self.init_edit_menu()
        self.init_pref_menu()
        
        self.lay.addWidget(self.menu)
    
    def init_pref_menu(self):
        self.pref_menu = QMenu('Prefere&nces')
        
        toggle_wordwrap = QAction('Toggle W&ord Wrap', self)
        fontsize = QAction('Change font size..', self)
        fontsize.triggered.connect(self.font_size_menu)
        
        font_menu = QMenu('Font style', self)
        
        arial = QAction('Arial', self)
        sansserif = QAction('MS Sans Serif', self)
        serif = QAction('MS Serif', self)
        comicsans = QAction('Comic Sans MS', self)
        calibri = QAction('Calibri', self)
        consolas = QAction('Consolas', self)
        
        segoe = QMenu('Segoe...', self)
        
        segoe_light = QAction('Segoe UI Light', self)
        segoe_normal = QAction('Segoe UI', self)
        segoe_symbol = QAction('Segoe UI Symbol', self)
        
        segoe_light.triggered.connect(lambda: self.change_textarea_font('Segoe UI Light', self.fsize))
        segoe_normal.triggered.connect(lambda: self.change_textarea_font('Segoe UI', self.fsize))
        segoe_symbol.triggered.connect(lambda: self.change_textarea_font('Segoe UI Symbol', self.fsize))
        
        segoe.addActions([segoe_light, segoe_normal, segoe_symbol])
        
        arial.triggered.connect(lambda: self.change_textarea_font('Arial', self.fsize))
        sansserif.triggered.connect(lambda: self.change_textarea_font('MS Sans Serif', self.fsize))
        serif.triggered.connect(lambda: self.change_textarea_font('MS Serif', self.fsize))
        comicsans.triggered.connect(lambda: self.change_textarea_font('Comic Sans MS', self.fsize))
        calibri.triggered.connect(lambda: self.change_textarea_font('Calibri', self.fsize))
        consolas.triggered.connect(lambda: self.change_textarea_font('Consolas', self.fsize))
        
        
        font_menu.addActions([arial, sansserif, serif, comicsans, calibri, consolas])
        font_menu.addMenu(segoe)
        
        self.pref_menu.addActions([toggle_wordwrap, fontsize])
        self.pref_menu.addMenu(font_menu)
        
        self.menu.addMenu(self.pref_menu)
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        if not self.is_saved:
            reply = self.ask_yes_no('File is not saved, Save it before closing?')
            
            if reply is True:
                self.save_file()
            
            elif reply is False:
                pass
            
            else:
                a0.ignore()
                return
        
        a0.accept()
        
    def font_size_menu(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Font size")
        dialog.resize(300, 200)
        
        def save_quit(v):
            self.fsize = slider.value()
            self.change_textarea_font(self.text_area.fontFamily(), self.fsize)
            dialog.close()
        
        lay = QVBoxLayout(dialog)
        
        lbl = QLabel("Change font size:")
        
        count_lbl = QLabel(f'Font size: {self.fsize}')
        
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setValue(self.fsize)
        slider.setMinimum(5)
        slider.setMaximum(70)
        slider.valueChanged.connect(lambda: count_lbl.setText(f'Font size: {slider.value()}'))
        
        ok_btn = QPushButton('Ok')
        
        cancel_btn = QPushButton('Cancel')
        
        ok_btn.clicked.connect(save_quit)
        cancel_btn.clicked.connect(dialog.close)
        
        btn_lay = QHBoxLayout()
        
        btn_lay.addWidget(ok_btn)
        btn_lay.addWidget(cancel_btn)
        
        lay.addWidget(lbl)
        lay.addWidget(count_lbl)
        lay.addWidget(slider)
        lay.addLayout(btn_lay)
        
        dialog.setLayout(lay)
        
        dialog.show()
    
    def init_file_menu(self):
        self.file_menu = QMenu('&File', self)
        
        save = QAction('&Save', self)
        save.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_S))
        
        open = QAction('&Open', self)
        open.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_O))
        
        saveas = QAction('S&ave as', self)
        saveas.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_S))
        
        new = QAction('&New', self)
        new.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_N))
        
        copy_path = QAction('Co&py file path', self)
        
        
        new.triggered.connect(self.new_file)
        save.triggered.connect(self.save_file)
        saveas.triggered.connect(self.saveas_file)
        open.triggered.connect(self.open_file)
        copy_path.triggered.connect(self.copy_file_path)
        
        
        self.file_menu.addAction(save)
        self.file_menu.addAction(saveas)
        self.file_menu.addAction(open)
        self.file_menu.addAction(new)
        self.file_menu.addAction(copy_path)
        
        self.menu.addMenu(self.file_menu)
    
    def init_edit_menu(self):
        self.edit_menu = QMenu("Edit", self)
        
        undo = QAction('Undo', self)
        undo.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Z))
        undo.triggered.connect(self.text_area.undo)
        
        redo = QAction('Redo', self)
        redo.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Y))
        redo.triggered.connect(self.text_area.redo)
        
        cut = QAction('Cut', self)
        cut.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_X))
        cut.triggered.connect(self.text_area.cut)
        
        copy = QAction('Copy', self)
        copy.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_C))
        copy.triggered.connect(self.text_area.copy)
        
        paste = QAction('Paste', self)
        paste.setShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_V))
        paste.triggered.connect(self.text_area.paste)
        
        self.edit_menu.addActions([
            undo, redo,
            cut, copy,
            paste
        ])
        
        self.menu.addMenu(self.edit_menu)
    
    def copy_file_path(self):
        if self.path == 'new':
            QMessageBox.critical(self, 'Problem', 'You have not saved the file, Please open a file or save this file first')
            return
        
        clip = app.clipboard()
        
        clip.setText(self.path)
    
    def save_file(self):
        if self.path == 'new':
            self.saveas_file()
            return
            
        with open(self.path, 'w') as f:
            f.write(self.text_area.toPlainText())

        self.is_saved = True
        QMessageBox.information(self, "Success", 'Succesfully saved file.')
    
    def saveas_file(self):
        dialog = QFileDialog(self)
        options = QFileDialog.Option.DontUseSheet
        
        filename, _ = dialog.getSaveFileName(self, initialFilter=self.initialFilter, options=options)
        
        if filename:
            with open(filename, 'w' if exists(filename) else 'x') as f:
                f.write(self.text_area.toPlainText())
            
            self.path = filename
            QMessageBox.information(self, "Success", 'Succesfully saved file.')
            self.is_saved = True
    
    def open_file(self):
        if not self.is_saved:
            reply = self.ask_yes_no("File is not saved! Would you like to save it?")
            
            if reply is True:
                self.save_file()
            
            elif reply is False:
                pass
            
            else:
                return
        
        dialog = QFileDialog()
        
        file, _ = dialog.getOpenFileName()
        
        if file:
            with open(file, 'r') as f:
                self.text_area.setText(f.read())
            
            self.path = file
            self.is_saved = True
    
    def ask_yes_no(self, msg: str):
        reply = QMessageBox.question(self, "Bean Text", msg, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel, QMessageBox.StandardButton.Cancel)
        
        if reply == QMessageBox.StandardButton.No:
            return False
        
        elif reply == QMessageBox.StandardButton.Yes:
            return True
        
        else:
            return 0
    
    def new_file(self):
        if not self.is_saved:
            reply = self.ask_yes_no("File is not saved, Would you like to save it?")
            
            if reply:
                print("not implemented")
            
            elif reply is False:
                pass
            
            else:
                return
        
        self.text_area.clear()
        self.is_saved = True
    
    def areatextChanged(self) -> None:
        self.is_saved = False

class TextArea(QTextEdit):
    def __init__(self, p: Main, t=''):
        super().__init__(t)
        
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_QuoteDbl:
            c = self.textCursor()
            
            c.insertText('""')
            
            c.movePosition(c.MoveOperation.Left, c.MoveMode.MoveAnchor, 1)

            self.setTextCursor(c)
        elif e.key() == Qt.Key.Key_Apostrophe:
            c = self.textCursor()
            
            c.insertText('\'\'')
            
            c.movePosition(c.MoveOperation.Left, c.MoveMode.MoveAnchor, 1)

            self.setTextCursor(c)
        
        elif e.key() == Qt.Key.Key_BraceLeft:
            c = self.textCursor()
            
            c.insertText('{}')
            
            c.movePosition(c.MoveOperation.Left, c.MoveMode.MoveAnchor, 1)

            self.setTextCursor(c)
        
        elif e.key() == Qt.Key.Key_BracketLeft:
            c = self.textCursor()
            
            c.insertText('[]')
            
            c.movePosition(c.MoveOperation.Left, c.MoveMode.MoveAnchor, 1)

            self.setTextCursor(c)
        
        elif e.key() == Qt.Key.Key_Asterisk:
            c = self.textCursor()
            
            c.insertText('**')
            
            c.movePosition(c.MoveOperation.Left, c.MoveMode.MoveAnchor, 1)

            self.setTextCursor(c)
        
        elif e.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return]:
            c = self.textCursor()
            
            try:
                c.movePosition(c.MoveOperation.Left, c.MoveMode.KeepAnchor, 4)
                
                if c.hasSelection():
                    if c.selectedText() == 'comp':
                        self.insert_completion_to_area(c, "completed ")
                        self.setTextCursor(c)
                    
                    elif c.selectedText() == 'dict':
                        self.insert_completion_to_area(c, "dictionary ")
                        self.setTextCursor(c)
                    
                    elif c.selectedText() == 'thrw':
                        self.insert_completion_to_area(c, "there were ")
                        self.setTextCursor(c)
                    
                    elif c.selectedText() == 'engl':
                        self.insert_completion_to_area(c, "english ")
                        self.setTextCursor(c)
                    
                    elif c.selectedText() == 'thsd':
                        self.insert_completion_to_area(c, ' said ')
                        c.movePosition(QTextCursor.MoveOperation.Left, QTextCursor.MoveMode.MoveAnchor, 6)
                        self.setTextCursor(c)
                    
                    else:
                        c.movePosition(c.MoveOperation.EndOfLine, c.MoveMode.MoveAnchor)
                        c.movePosition(c.MoveOperation.StartOfLine, c.MoveMode.KeepAnchor)
                        
                        c.insertText(f'{c.selectedText()}\n')
                        
                        self.setTextCursor(c)
                else:
                    super().keyPressEvent(e)
            except Exception:
                super().keyPressEvent(e)
        
        elif e.key() == Qt.Key.Key_ParenLeft:
            c = self.textCursor()
            
            c.insertText('()')
            
            c.movePosition(c.MoveOperation.Left, c.MoveMode.MoveAnchor, 1)

            self.setTextCursor(c)
        
        else:
            super().keyPressEvent(e)

    def insert_completion_to_area(self, c: QTextCursor, completion: str):
        c.removeSelectedText()
        c.insertText(completion)


if __name__ == '__main__':
    app = QApplication([])
    
    main = Main()
    main.setWindowTitle('Bean Text')
    main.resize(800, 600)
    
    
    if len(argv) > 1:
        try:
            main.path = argv[1]
            main.text_area.setText(open(main.path).read())
            main.is_saved = True
        
        except Exception:
            pass
    
    main.show()
    
    app.exec()
