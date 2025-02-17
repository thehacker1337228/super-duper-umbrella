from services.user_service import UserService, UserDto
from services.note_service import NoteService, NoteDto
from enum import Enum
import json
import random


class SessionState(Enum):
    LOGIN = "login"
    MENU = "menu"
    ADD_NOTE = "add_note"
    NOTES_LIST = "notes_list"
    DEL_NOTE = "del_note"
    EDIT_NOTE = "edit_note"


class Menu:
    def __init__(self, need_init=False):
        self.note_service = NoteService()
        self.user_service = UserService()

        if need_init:
            self.note_service.init_data()
            self.user_service.init()  # инициализируем табличку с юзерами

        self.tg_id = self.login()
        self.user = self.user_service.get(self.tg_id)  # dto object of User
        self.user_id = UserDto.to_model(self.user)[-1]

        state = SessionState.LOGIN.value
        self.user.state = state
        self.user_service.update(self.user)  # апдейтим стейт

    def login(self):
        while True:
            print("Введите свой telegram id\n Либо 111, либо 222, либо 333")
            tg_id = input()
            if tg_id.isnumeric() and int(tg_id) in (111, 222, 333):
                return tg_id

            print("tg_id должно быть числом и равняться 111/222/333")

    def start(self):
        while True:
            user = self.user_service.get(self.tg_id)  # раскатываем дто объект юзера обязательно заново
            state = SessionState.MENU.value
            user.state = state
            self.user_service.update(user)  # апдейтим стейт

            print("Заметки\n1.Добавить\n2.Мои заметки\n3.Тыкалка\n4.Удалить заметки\n5.Редактировать заметки\n6.Выход")
            command = input("Plz write 1-3: ")
            if command == "1":
                self.add()
            elif command == "2":
                self.show_all()
            elif command == "3":
                self.tikalka()
            elif command == "4":
                self.delete()
            elif command == "5":
                self.edit()
            elif command == "6":
                print("Поки споки")
                exit()
            else:
                print("Неверная команда!")

    def edit(self):
        print('Выберите заметку для редактирования: ')
        self.show_all()

        user = self.user_service.get(self.tg_id)  # раскатываем дто объект юзера обязательно заново
        state = SessionState.EDIT_NOTE.value
        user.state = state
        self.user_service.update(user)  # апдейтим стейт

        index = input("Введи note_id заметки (первый столбец таблицы):")
        json_data = json.dumps({"edit_index": index}, ensure_ascii=False)
        user.json_data = json_data
        self.user_service.update(user)  # апдейтим json

        note = self.note_service.get_note(index)

        content = input("Редактирование заметки: ")
        note.content = content
        json_data = json.dumps({"edit_content": content}, ensure_ascii=False)
        user.json_data = json_data
        self.user_service.update(user)  # апдейтим json
        self.note_service.update(note)
        print("Заметка обновлена!")

        json_data = json.dumps({"edit_done": content}, ensure_ascii=False)
        user.json_data = json_data
        self.user_service.update(user)  # апдейтим json
        return

    def delete(self):
        print("Выбери заметку, которую хочешь удалить!")
        self.show_all()

        user = self.user_service.get(self.tg_id)  # раскатываем дто объект юзера обязательно заново
        state = SessionState.DEL_NOTE.value
        user.state = state
        self.user_service.update(user)  # апдейтим стейт

        index = input("Введи note_id заметки (первый столбец таблицы):")
        json_data = json.dumps({"del_index": index}, ensure_ascii=False)
        user.json_data = json_data
        self.user_service.update(user)  # апдейтим json

        question = input("Вы действительно хотите удалить заметку?")
        self.note_service.delete(index)
        json_data = json.dumps({"del_done": index}, ensure_ascii=False)
        user.json_data = json_data
        self.user_service.update(user)  # апдейтим json

        print("Заметка удалена")
        return

    def add(self):

        user = self.user_service.get(self.tg_id)  # раскатываем дто объект юзера обязательно заново
        state = SessionState.ADD_NOTE.value
        user.state = state
        self.user_service.update(user)  # апдейтим стейт

        title = input("Введите название заметки\n")
        json_data = json.dumps({"add_title": title}, ensure_ascii=False)
        user.json_data = json_data
        self.user_service.update(user)  # апдейтим json

        content = input("Введите текст\n")
        json_data = json.dumps({"add_content": content}, ensure_ascii=False)
        user.json_data = json_data
        self.user_service.update(user)  # апдейтим json

        note = NoteDto(self.user_id, title, content)
        self.note_service.add(note)
        # print(note.user_id)
        print("Заметка создана")

        json_data = json.dumps({"add_done": content}, ensure_ascii=False)
        user.json_data = json_data
        self.user_service.update(user)  # апдейтим json
        return

    def show_all(self):
        notes = self.note_service.get_all(self.user_id)

        user = self.user_service.get(self.tg_id)  # раскатываем дто объект юзера обязательно заново
        state = SessionState.NOTES_LIST.value
        user.state = state
        self.user_service.update(user)  # апдейтим стейт

        print("=====[ Заметки ]=====")
        for note in notes:
            note.print()
        print()

    def tikalka(self):
        print("Случайное число от 1 до 100:", random.randint(1, 100), "\nВызываю снова меню", "\n--------------")
        return


def main():
    menu = Menu(True)
    menu.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Выходим")
