# Shazamio Block
import asyncio  # Модуль для корректной работы библиотеки Shazamio
from shazamio import Shazam  # SHAZAM API

# Блок звукозаписи
import soundcard as sc
import soundfile as sf
# from pythoncom import CoInitializeEx, CoUninitialize

# PyQt5 Block
from PyQt5.QtWidgets import (QApplication, QFileDialog, QInputDialog, QWidget, QLabel, QPushButton, QScrollArea,
                             QHBoxLayout, QVBoxLayout, QMainWindow)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from design import UI_PyJam, UI_Charts, UI_DataBaseWindow, UI_Dialog  # Дизайн приложения
import sys

# Модуль для загрузки картинки с интернета
from urllib import request

# Модуль для копирования ссылки в буфер обмена
import pyperclip

# Работа с базой данных
import sqlite3

# Для проверки: существует ли база данных в директории приложения:
from pathlib import Path

# Для отображения даты в базе данных:
from datetime import datetime

""" 
    Переменные, которые используется в программе: ссылки, словарь, функции
"""
# Создание переменных со ссылками на картинки (я специально не сокращаю ссылки, иначе они могут не загрузиться):
logotype = 'https://is2-ssl.mzstatic.com/image/thumb/Purple114/v4/2a/a3/72/2aa37241-d9ee-cccd-cce3-be719dd5c1a7/source/512x512bb.jpg'
recording = 'https://play-lh.googleusercontent.com/EiB8nFwIAQxl8JrfoaNVIXSM7FZZ108NmJ_D0Eqyb1utmDLe3FgKU8p7OEwAhnDWzl8'
recognizing = 'https://img.freepik.com/premium-photo/blue-question-mark-and-search-magnifying-glass-symbol-concept-on-find-faq-background-with-discovery-or-research-magnifier-object-3d-rendering_79161-1827.jpg'
failed = 'https://n1s2.hsmedia.ru/86/77/23/867723f3250120d3e3b7fea6f0b374e3/600x600_0x0a330c2a_6671027011600959275.jpeg'

# Для работы с добавлением информации в таблицу charts (в БД):
countries = {'RU': 'Russia', 'IT': 'Italy', 'FR': 'France', 'DE': 'Germany',
             'US': 'USA', 'ES': 'Spain'}


# Заменяем одни кавычки на другие (для записи в БД во избежание ошибки)
def change_quotes(string):
    while '"' in string:
        string = string.replace('"', '«', 1).replace('"', '»', 1)
    return string


"""
    Загружаем изображение из интернета.
    Пример работы: получаем ссылку на изображение, копируем его и отображаем на экране. Используется во всех классах.
"""


def show_track_image(url, label, w, h):
    # Read a URL, get an image
    # Блок try-except нужен для того, чтобы избежать ошибки при проверки сертификата. (Такое бывает на некоторых ПК)
    try:
        data = request.urlopen(url).read()

        pixmap = QPixmap()  # create a QPixMap object
        pixmap.loadFromData(data)  # paste image to pixmap object
        pixmap = pixmap.scaled(w, h)  # convert pixmap image size to 311x310

        label.setPixmap(pixmap)  # show image on the app screen
    except:
        pass


"""
    Копирование ссылки в буфер обмена. Функция использует модуль pyperclip.
    После того, как пользователь смог распознать песню, он может нажать на соответствующую кнопку, чтобы скопировать
    ссылку на трек в Shazam. Если пользователь не смог распознать песню, кнопка ничего не будет делать.
    PS: Можно добавить надпись об копировании ссылки и об её отсутствии (НЕ БУДЕТ РЕАЛИЗОВАНО)
"""


def copyLink(var):
    if var is not None:
        pyperclip.copy(var)


""" 
    Блок работы с датой.
    Дата используется в качестве ячейки в базе данных, а также при отображении в окне показа базы данных.
    Используется метод datetime из библиотеки datetime.
"""


# Текущая дата (дата распознавания трека). Такой формат записывается в ячейку базы данных <date>:
def get_current_date():
    date = datetime.now().isoformat().split('T')
    return f'{date[0]}, {date[1][:5]}'


# Конвертируем дату для её отображения в окне базы данных. (Примечание: cd, tm - current date, time (FOR DATABASE UI)):
def convert_date(current_date):
    current_date = current_date.split(', ')
    cd, tm = current_date[0].split('-')[1:], current_date[1]

    dictionary = {'01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля', '05': 'мая', '06': 'июня',
                  '07': 'июля', '08': 'августа', '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
                  }
    return f'{cd[1]} {dictionary[cd[0]]}, {tm}'


""" 
    Блок Asyncio.
    Asyncio "жизненно" необходим для стабильной работы модуля Shazamio и приложения в целом.
    Используется для создания Async- и Await- функций, а также при распознавании музыки.
"""
# Создаём новую переменную Asyncio:
loop = asyncio.new_event_loop()

# https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

"""
    Блок всех функций, работающих с библиотекой Shazamio.
    Представлены функции распознавания музыки, 
    а также поиск первой позиции чартов Российского города, некоторой страны и всего мира!
"""


# Функция для распознавания песни (BY SHAZAMIO)
async def recognizeShazamio(filename='out.wav'):
    shazam = Shazam()

    # Recognize a song
    out = await shazam.recognize_song(filename)
    if out['matches']:
        id_ = f'https://www.shazam.com/ru/track/{out["matches"][0]["id"]}'  # convert song id to link to song in shazam
        track = out['track']
    else:
        return False

    return id_, track['title'], track['subtitle'], track['images']['coverart']


# Функция возвращает самый популярный трек из введенного пользователем города на данный момент (по умолчанию - RU, МСК):
async def top_of_city(city):
    shazam = Shazam()

    try:
        out = await shazam.top_city_tracks(country_code='RU', city_name=city, limit=1)
        track = out['tracks'][0]
        id_ = f'https://www.shazam.com/ru/track/{track["key"]}'  # convert song id to link to song in shazam

        return id_, track['title'], track['subtitle'], track['images']['coverart']
    except:
        return False


# Функция возвращает самый популярный трек из введенной пользователем страны на данный момент:
async def top_of_country(country):
    shazam = Shazam()

    try:
        out = await shazam.top_country_tracks(country, 1)
        track = out['tracks'][0]
        id_ = f'https://www.shazam.com/ru/track/{track["key"]}'  # convert song id to link to song in shazam

        return id_, track['title'], track['subtitle'], track['images']['coverart']
    except:
        return False


# Функция возвращает самый популярный трек в мире на данный момент:
async def top_of_world():
    shazam = Shazam()
    out = await shazam.top_world_tracks(limit=1)
    track = out['tracks'][0]
    id_ = f'https://www.shazam.com/ru/track/{track["key"]}'  # convert song id to link to song in shazam

    return id_, track['title'], track['subtitle'], track['images']['coverart']


"""
    Следующий блок является собранием всех потоков, 
    необходимых для бесперебойной работы основного экрана приложения.
    (по простому - Созданы, чтобы интерфейс не тормозил при обработке нажатия одной из кнопок):
"""


# QThread - поток для записи звука с компьютера
class AudioRecordingThread(QThread):
    mysignal = pyqtSignal(int)

    def __init__(self):
        QThread.__init__(self)
        self.good = 1  # Для проверки: успешна ли прошла звукозапись. Если возникла ошибка, то становится нулём

    def run(self):
        OUTPUT_FILE_NAME = "out.wav"  # file name
        SAMPLE_RATE = 48000  # [Hz] sampling rate
        RECORD_SEC = 6  # [sec] duration recording audio

        try:
            with sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).recorder(
                    samplerate=SAMPLE_RATE) as mic:
                # record audio with loopback from default speaker.
                data = mic.record(numframes=SAMPLE_RATE * RECORD_SEC)

                # change "data=data[:, 0]" to "data=data", if you would like to write audio as multiple-channels.
                sf.write(file=OUTPUT_FILE_NAME, data=data[:, 0], samplerate=SAMPLE_RATE)

        except RuntimeError:
            self.good = -1

        self.mysignal.emit(self.good)


# QThread - поток для распознавания музыки
class RecognitionThread(QThread):
    mysignal = pyqtSignal(tuple)

    def __init__(self, filename='out.wav'):
        QThread.__init__(self)
        self.filename = filename

    def run(self):
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(recognizeShazamio(filename=self.filename))
        if not data:
            data = tuple()

        self.mysignal.emit(data)


"""
    Следующий блок является собранием всех потоков, 
    необходимых для бесперебойной работы ВТОРОСТЕПЕННОГО экрана приложения (Экран Чартов).
    (по простому - блок с потоками ВТОРОСТЕПЕННОГО экрана приложения. 
    Созданы, чтобы интерфейс не тормозил при обработке нажатия одной из кнопок):
"""


# QThread - поток для вывода самой популярной музыки в определённом городе (на данный момент):
class TopOfCity(QThread):
    mysignal = pyqtSignal(tuple)

    def __init__(self, city=None):
        QThread.__init__(self)
        self.city = city

    def run(self):
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(top_of_city(self.city))

        if not data:
            data = tuple()

        self.mysignal.emit(data)


# QThread - поток для вывода самой популярной музыки в определенной стране (на данный момент):
class TopOfCountry(QThread):
    mysignal = pyqtSignal(tuple)

    def __init__(self, country=None):
        QThread.__init__(self)
        self.country = country

    def run(self):
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(top_of_country(self.country))

        if not data:
            data = tuple()

        self.mysignal.emit(data)


# QThread - поток для вывода самой популярной музыки во всём мире (на данный момент):
class TopOfWorld(QThread):
    mysignal = pyqtSignal(tuple)

    def __init__(self):
        QThread.__init__(self)

    def run(self):
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(top_of_world())

        if not data:
            data = tuple()

        self.mysignal.emit(data)


""" 
    Основной класс приложения PyJam.
    Описывает все функции, методы и свойства главного окна приложения.
    Связан с другими окнами: вторым окном поиска первой позиции чартов (Charts), 
    а также с окном показа информации базы данных (DataBaseWindow).
"""

# Класс для диалога ввода данных (загружаем для него дизайн):
class InputDialog(QInputDialog, UI_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class PyJam(QMainWindow, UI_PyJam):
    """
        INIT BLOCK.
        Описывает фиксированный размер окна, все действующие потоки, связки кнопок с методами класса.
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Загрузка дизайна
        self.setWindowTitle('PyJam')
        self.setFixedSize(412, 572)  # Устанавливаем фиксированный размер окна: 412x572
        self.create_database()  # Создаём базу данных
        self.link = None  # Ссылка на трек (изначально ссылка отсутствует, появляется она после распознавания музыки)

        """ 
            QThread - Потоки. 
            Потоки созданы для предотвращения зависания графического интерфейса приложения во время обработки
            данных. Используются в методах класса приложения.
        """
        # Поток для записи аудио:
        self.audio_thread = AudioRecordingThread()
        self.audio_thread.mysignal.connect(self.recognize_song)

        # Поток для распознавания музыки:
        self.recognition_thread = RecognitionThread()
        self.recognition_thread.mysignal.connect(self.recognize_out)

        """ 
            Оставшаяся работа:
            Отображаем логотип PyJam,
            связываем кнопки с методами.
        """
        show_track_image(logotype, self.imageLabel, w=311, h=310)  # Отобразить логотип PyJam в окне

        # Создание связей кнопок и функций:
        self.recognizeSong_Button.clicked.connect(self.audio_recording)  # кнопка для распознавания музыки
        self.recognizeFile_Button.clicked.connect(self.recognize_file)  # кнопка для распознавания аудиофайла

        self.search_Button.clicked.connect(self.search)  # some functions (come up with)
        self.copyLink_Button.clicked.connect(self.copy_link)  # кнопка копирования ссылки в буфер обмена
        self.recognized_Button.clicked.connect(self.show_database)  # кнопка для отображения базы данных

    # Создаём базу данных:
    def create_database(self):
        if not Path('recognized.db').is_file():
            self.con = sqlite3.connect('recognized.db')
            cur = self.con.cursor()

            cur.execute("""CREATE TABLE recognized(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT,
                           imgLink TEXT, trackName TEXT, bandName TEXT, isFav BOOL, trackLink TEXT)""")

            cur.execute("""CREATE TABLE charts(id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT,
                           imgLink TEXT, trackName TEXT, bandName TEXT, extraInfo TEXT, isFav BOOL, tracklink TEXT)""")
        else:
            self.con = sqlite3.connect('recognized.db')

    """
        Следующие три функции связаны между собой и являются основополагающими в приложении.
        Связка auduo_recording -> recognize_song -> recognize_out:
        
          audio_recording [поток AudioRecordingThread] - записывает аудио поток с компьютера пользователя. (6 секунд)
          recognize_song [поток RecognitionThread] - распознает записанный звук / файл в базе данных Shazam.
          recongize_out - выводит информацию о распознанной песне или сообщение о нераспознании песни.
    """

    # Записываем аудио-дорожку с компьютера пользователя:
    def audio_recording(self):
        self.showTrackLabel.setText('Слушаем внимательно...')
        self.showBandLabel.clear()
        show_track_image(recording, self.imageLabel, w=311, h=310)
        self.audio_thread.start()

    # Распознаём записанное аудио или аудио-файл:
    def recognize_song(self, good, filename='out.wav'):
        # Сразу проверяем, успешна ли звукозапись. Если нет, то отображаем сообщение об ошибке на экран:
        if type(good) is not str:
            if good < 0:
                self.recognize_out(None)
                return

        self.recognition_thread.filename = filename
        self.showTrackLabel.setText('Распознаем песню...')
        self.showBandLabel.clear()
        show_track_image(recognizing, self.imageLabel, w=311, h=310)
        self.recognition_thread.start()

    # Выводим информацию после обработки песни:
    def recognize_out(self, info):
        data = info  # Получаем данные

        # Если распознавание успешно:
        if data:
            # ссылка на картинку трека, название трека, название исполнителя, ссылка на трек
            imgLink, trackName, bandName, trackLink = data[3], change_quotes(data[1]), change_quotes(data[2]), data[0]

            # Отображение названия трека:
            if len(trackName) > 38:
                self.showTrackLabel.setText(trackName[:38] + '...')
            else:
                self.showTrackLabel.setText(trackName)

            # Отображение названия исполнителя
            if len(bandName) > 38:
                self.showBandLabel.setText(bandName[:38] + '...')
            else:
                self.showBandLabel.setText(bandName)

            # Отображение картинки трека
            show_track_image(imgLink, self.imageLabel, w=311, h=310)

            self.link = trackLink  # Обновление ссылки

            # Вносим новые данные в БД:
            cur = self.con.cursor()
            cur.execute(f'''INSERT INTO recognized(date, imgLink, trackName, bandName, isFav, trackLink)
                           VALUES("{get_current_date()}", "{imgLink}", "{trackName}", "{bandName}", 0, 
                                  "{trackLink}")''')
            self.con.commit()

        # Если не удалась звукозапись:
        elif data is None:
            show_track_image(failed, self.imageLabel, w=311, h=310)
            self.showTrackLabel.setText('Ошибка звукозаписи...')
            self.showBandLabel.setText('Попробуйте ещё раз!')
            self.link = None

        # Распознавание не удалось:
        else:
            show_track_image(failed, self.imageLabel, w=311, h=310)
            self.showTrackLabel.setText('Не удаётся найти данный трек...')
            self.showBandLabel.setText('Попробуйте ещё раз!')
            self.link = None

    """
        Функция recognizeFile работает со связкой функций, описанной выше, 
        но в данном случае пропускается функция audio_recording, поскольку мы анализируем файл, а не записанный звук
        с компьютера пользователя.
    """
    def recognize_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Выберите аудио-', '',
                                                     "Audio (*.mp3 *.wav *.ogg *.aac, *.flac)",
                                                     options=QFileDialog.DontUseNativeDialog)[0]
        if filename != '':
            self.recognize_song(filename)

    """
        Метод, открывающий ещё одно окно в приложении.
        Это окно поможет пользователю найти первую позицию чартов 
        в определенном российском городе, некоторой стране и во всём мире!
    """

    def search(self):
        self.form = Charts()  # Объект окна
        self.form.show()  # Отображение окна
        self.close()  # Скрываем основное окно

    """
        Метод, открывающий окно в приложении, которое предоставляет информацию из базы данных.
        В базе данных хранится информация обо всех треках, которые смог распознать пользователь.
        По желанию можно добавлять распознанные треки в "избранное", а также удалять их.
        Также можно отсортировать треки по следующим критериям: 1. Все распознанные треки; 2. Избранное.
    """

    def show_database(self):
        self.db = DataBaseWindow()  # Объект окна
        self.db.show()  # Отображение окна
        self.close()

    # Копирование ссылки с помощью модуля pyperclip:
    def copy_link(self):
        copyLink(self.link)


"""
    Класс, описывающий окно для поиска чартов.
    Окно открывается при нажатии соответствующей кнопки на главном экране приложения.
    Полученный чарт вносится в БД в таблицу charts.
"""
class Charts(QMainWindow, UI_Charts):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # load design
        self.setFixedSize(412, 572)  # set fixed size 412x572
        self.link = None  # Ссылка на трек
        self.setWindowTitle('PyJam Чарты')

        """
            Переменная для внесения дополнительной информации о чарте, который получил пользователь.
            Изначально значение переменной - None. Она обновляется в зависимости от того, что за чарт нашёл
            пользователь (чарт города, страны или мира).
        """
        self.extraInfo = None

        # Соединяемся с БД
        self.con = sqlite3.connect('recognized.db')

        """ QThread - потоки """
        # Поток для нахождения мирового хита:
        self.worldTop_Thread = TopOfWorld()
        self.worldTop_Thread.mysignal.connect(self.show_information)

        # Поток для нахождения хита страны:
        self.countryTop_Thread = TopOfCountry()
        self.countryTop_Thread.mysignal.connect(self.show_information)

        # Поток для нахождения хита российского города:
        self.cityTop_Thread = TopOfCity()
        self.cityTop_Thread.mysignal.connect(self.show_information)

        # Отобразить логотип PyJam в окне
        show_track_image(logotype, self.imageLabel, w=311, h=310)

        # Соединяем кнопки:
        self.worldTop_Button.clicked.connect(self.get_world_hit)
        self.countryTop_Button.clicked.connect(self.get_country_hit)
        self.cityTop_Button.clicked.connect(self.get_city_hit)
        self.copyLink_Button.clicked.connect(self.copy_link)

    # Функция для поиска мирового хита:
    def get_world_hit(self):
        show_track_image(recognizing, self.imageLabel, w=311, h=310)
        self.showTrackLabel.setText('Ищем мировой хит...')
        self.showBandLabel.clear()
        self.extraInfo = 'The World Hit'
        self.worldTop_Thread.start()

    # Функция для поиска хита страны, выбранной пользователем (список предоставлен в форме):
    def get_country_hit(self):

        # Форма для выбора страны:
        country, ok_pressed = InputDialog().getItem(self, "Топ страны", "Выберите страну:",
                                                   ('RU', 'US', 'DE', 'FR', 'IT', 'ES'), 0, False)

        # Если нажата клавиша ОК:
        if ok_pressed:
            self.showTrackLabel.setText('Ищем хит вашей страны...')
            self.showBandLabel.clear()  # Очищаем надпись названия исполнителя

            # Загружаем изображение:
            show_track_image(recognizing, self.imageLabel, w=311, h=310)

            self.countryTop_Thread.country = country  # Добавляем в наш поток избранную информацию о стране:
            self.extraInfo = f'Hit in {countries[country]}'

            self.countryTop_Thread.start()  # Запуск потока
        else:
            self.clear()  # Очищение всего, если пользователь не решился на поиск чарта

    # Функция для поиска хита города (пользователем пишется название российского города на английском языке).
    # В этой функции учтено событие, при котором пользователем вводит несуществующий город (реализовано далее):
    def get_city_hit(self):
        # Форма для информации:
        city, ok_pressed = InputDialog().getText(self, 'Топ города', 'Введите название Российского города на англ. яз:')

        # Нажатие кнопки ОК:
        if ok_pressed:
            self.showTrackLabel.setText('Находим хит вашего города...')
            self.showBandLabel.clear()  # Очищаем надпись названия исполнителя

            show_track_image(recognizing, self.imageLabel, w=311, h=310)  # Загружаем ссылку:
            self.cityTop_Thread.city = city  # Добавляем в наш поток избранную информацию о городе:
            self.extraInfo = f'Hit in {city}'  # Доп.информация
            self.cityTop_Thread.start()  # Запуск потока
        else:
            self.clear()  # Очищение всего, если пользователь не решился на поиск чарта

    # Отображение информации о чарте, который искал пользователь:
    def show_information(self, information):
        data = information  # Получаем всю необходимую информацию в виде списка

        # Если полученный список не пустой (содержит информацию, что свидетельствует об успешном нахождении чарта):
        if data:
            # Ссылка на изображение трека, название трека, название исполнителя, ссылка на трек:
            imgLink, trackName, bandName, trackLink = data[-1], change_quotes(data[1]), change_quotes(data[2]), data[0]

            # Отображение названия трека
            if len(trackName) > 38:
                self.showTrackLabel.setText(trackName[:38] + '...')
            else:
                self.showTrackLabel.setText(trackName)

            # Отображение названия исполнителя
            if len(bandName) > 38:
                self.showBandLabel.setText(bandName[:38] + '...')
            else:
                self.showBandLabel.setText(bandName)

            # Отображение картинки трека
            show_track_image(imgLink, self.imageLabel, w=311, h=310)
            self.link = trackLink  # Копирование ссылку в переменную

            # Создаём курсор для БД и выполняем запрос:
            cur = self.con.cursor()
            cur.execute(f'''INSERT INTO charts(date, imgLink, trackName, bandName, extraInfo, isFav, trackLink)
                                       VALUES("{get_current_date()}", "{imgLink}", "{trackName}", "{bandName}",
                                               "{self.extraInfo}", 0, "{trackLink}")''')
            self.con.commit()

        # Если мы не получили информацию:
        else:
            show_track_image(failed, self.imageLabel, w=311, h=310)
            self.showTrackLabel.setText('Ошибка поиска!')
            self.showBandLabel.setText('Введите корректные данные!')
            self.link = None
        self.extraInfo = None

    # Очищение картинки, названия трека и исполнителя, ссылки, которая может копироваться в буфер обмена пользователя:
    def clear(self):
        show_track_image(logotype, self.imageLabel, w=311, h=310)
        self.showTrackLabel.setText('Нажмите кнопку, чтобы начать')
        self.showBandLabel.setText('А дальше - произойдёт настоящая магия...')
        self.link = None

    # Копирование ссылки с помощью модуля pyperclip:
    def copy_link(self):
        copyLink(self.link)

    # При закрытии окна, отображаем основное окно:
    def closeEvent(self, event):
        self.close()
        self.main = PyJam()
        self.main.show()


"""
    Класс, описывающий окно для отображения информации обо всех распознанных пользователем треках, а также всех чартов, 
    которые он искал.
    Окно открывается при нажатии соответствующей кнопки на главном экране приложения.
    В базе данных имеются две таблицы: recognized - список распознанных треков, а также    
                                       charts - список чартов, которые нашёл пользователь.
                                       
    В таблице recognized можно добавлять треки в избранное.
    Во всех таблицах можно удалить информацию о любом треке. Изменять саму информацию нельзя.
"""
class DataBaseWindow(QMainWindow, UI_DataBaseWindow):
    def __init__(self, table='R', command="""SELECT * FROM recognized"""):
        super().__init__()
        self.setupUi(self)  # Загружаем дизайн окна:
        self.update_db(command=command)  # Получаем данные из базы данных:

        # Переменная table нужна для того, чтобы после обновления окна, в котором выполнял действие пользователь,
        # открывать это же окно. Типы данных: R, F, C (Recognized, Favourite, Charts)
        self.table = table

        """
            Список всех кнопок "избранное", всех кнопок "удалить", всех id в таблице RECOGNIZED и таблице CHARTS, а
            также всех булевых значений, определяющих, находится ли трек в таблице CHARTS.
        """
        self.buttonFavList = []
        self.buttonDelList = []
        self.id_list = []  # все id в RECOGNIZED
        self.is_chart_list = []  # Необходимо для определения: из какой таблицы получены данные

        # Работаем с отображением данных
        self.initUI()

        # Задаём размеры окна:
        self.setGeometry(600, 100, 815, 800)  # Размер окна
        self.setWindowTitle('Распознанные треки')  # Название окна

    # Создаём интерфейс, связываем кнопки с функциями:
    def initUI(self):
        # Блок создания кнопки для отображения всех распознанных треков:
        self.allRecognizedTracks_Button = QPushButton('Все распознанные треки', self)
        self.allRecognizedTracks_Button.resize(200, 200)
        self.allRecognizedTracks_Button.clicked.connect(self.showAllRecognizedTracks)

        # Блок создания кнопки для отображения всех избранных пользователем треков:
        self.favouritesTracks_Button = QPushButton('Избранное', self)
        self.favouritesTracks_Button.resize(200, 200)
        self.favouritesTracks_Button.clicked.connect(self.showAllFavouritesTracks)

        # Блок создания кнопки для отображения всех чартов, которые нашёл пользователь:
        self.foundCharts_Button = QPushButton('Чарты', self)
        self.foundCharts_Button.resize(200, 200)
        self.foundCharts_Button.clicked.connect(self.showAllFoundCharts)

        # Scroll Area which contains the widgets, set as the centralWidget.
        # Виджет для возможности "скроллить" таблицу:
        self.scroll = QScrollArea()

        # Widget that contains the collection of Vertical Box.
        # Виджет, содержащий коллекцию вертикальных блоков:
        self.widget = QWidget()

        # The Vertical Box that contains the Horizontal Boxes of labels and buttons.
        # Вертикальный блок, содержащий горизонтальные блоки для всех объектов QLabel и кнопок QPushButton's:
        self.databaseVerticalLayout = QVBoxLayout()
        self.databaseVerticalLayout.setSpacing(12)  # Задаём межстрочный интервал - 12 пикселей.
        self.databaseVerticalLayout.setAlignment(Qt.AlignTop)  # Для отображения информации сверху вниз:

        # Горизонтальный блок для кнопок. Добавляется на экран самым первым:
        self.databaseButtonLayout = QHBoxLayout()

        # Добавляем кнопки в горизонтальный блок:
        self.databaseButtonLayout.addWidget(self.allRecognizedTracks_Button)
        self.databaseButtonLayout.addWidget(self.favouritesTracks_Button)
        self.databaseButtonLayout.addWidget(self.foundCharts_Button)

        # Добавляем горизонтальный блок в основной вертикальный:
        self.databaseVerticalLayout.addLayout(self.databaseButtonLayout)

        # Добавляем ряд, содержащий информацию о распознанном треке или чарте (Перебираем все данные из таблицы):
        for i in range(len(self.database)):
            # Данные ряда:
            data = self.database[i]

            # Проверяем, является ли полученные данные данными чарта:
            is_chart = len(data) == 8

            # id колонки, время распознавания / нахождения, название трека, название исполнителя:
            id_ = data[0]
            time = data[1]
            track_name = data[3]
            band_name = data[4]

            # Если трек является распознанным, а не чартом, и при этом колонка isFav истинна,
            # то отображаем после названия трека звездочку, которая показывает пользователю то, что трек избран:
            if not is_chart and data[5]:
                track_name += ' ⭐'
            elif is_chart:
                track_name += ' 🔝'

            # Создаём ряд для информации (горизонтальный блок)
            self.databaseRowLayout = QHBoxLayout()

            # Создаём виджет для отображения картинки распознанного трека:
            self.imageLabel = QLabel(self)
            show_track_image(self.images[i], self.imageLabel, w=100, h=100)  # Загружаем картинку:
            self.imageLabel.setMaximumSize(100, 100)  # Задаём максимальную ширину и высоту

            # Вертикальный блок для отображения информации о распознанной музыке / песне:
            self.rowTrackInfoVLayout = QVBoxLayout()
            self.rowTrackInfoVLayout.addWidget(QLabel(track_name, self))  # Название трека
            self.rowTrackInfoVLayout.addWidget(QLabel(band_name, self))  # Название исполнителя
            if is_chart:  # Если информация является информацией чарта, то также отображем доп. информацию в ряду:
                self.rowTrackInfoVLayout.addWidget(QLabel(data[5], self))
            self.rowTrackInfoVLayout.addWidget(QLabel(convert_date(time), self))  # Дата распознавания / нахождения

            # Горизонтальный блок для отображения кнопок ("избранное", "удалить").
            # Также, добавляем все кнопки и id ряда в соответствующие списки:
            self.rowButtonHLayout = QHBoxLayout()

            # Если полученная информация не является информацией чарта, то добавляем кнопку "избранное" в ряд:
            if not is_chart:
                favouriteButton = QPushButton('⭐', self)  # Избранное
                favouriteButton.setFixedSize(50, 50)
                favouriteButton.clicked.connect(self.makeFavouriteTrack)
                self.buttonFavList.append(favouriteButton)
                self.rowButtonHLayout.addWidget(favouriteButton)  # Добавляем кнопку в блок:

            # Инициализация кнопки удаления, привязка к ней функции удаления из БД:
            deleteButton = QPushButton('🗑️', self)  # Удалить
            deleteButton.setFixedSize(50, 50)
            deleteButton.clicked.connect(self.delTrack)
            self.buttonDelList.append(deleteButton)  # Добавляем кнопку удалить в массив:
            self.rowButtonHLayout.addWidget(deleteButton)  # Добавляем кнопку в блок:

            # Добавляем id и булевое значение (проверка на чарт) в соответствующие массивы:
            self.id_list.append(id_)
            self.is_chart_list.append(is_chart)

            # Добавляем всю необходимую информацию в наш ряд БД:
            self.databaseRowLayout.addWidget(self.imageLabel)
            self.databaseRowLayout.addLayout(self.rowTrackInfoVLayout)
            self.databaseRowLayout.addLayout(self.rowButtonHLayout)

            # Добавляем ряд в основной вертикальный блок:
            self.databaseVerticalLayout.addLayout(self.databaseRowLayout)

        # Отображаем основной вертикальный блок со всей информацией:
        self.widget.setLayout(self.databaseVerticalLayout)

        # Задаем параметры для scroll-бара:
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # Пролистывание всегда включено
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Горизонтальное пролистывание отключено
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        # Делаем scroll-бар центральным виджетом:
        self.setCentralWidget(self.scroll)

        # Отображение окна:
        self.show()

    # Функция отображает все распознанные пользователем треки:
    def showAllRecognizedTracks(self):
        self.hide()
        self.__init__()
        self.setWindowTitle('Распознанные треки')

    # Функция отображает все избранные треки, которые распознал пользователь:
    def showAllFavouritesTracks(self):
        self.hide()
        self.__init__('F', """SELECT * FROM recognized WHERE isFav = 1""")
        self.setWindowTitle('Избранное')

    # Функция отображает все чарты, которые распознал пользователь:
    def showAllFoundCharts(self):
        self.hide()
        self.__init__('C', """SELECT * FROM charts""")
        self.setWindowTitle('Чарты')

    # Сделать трек избранным / убрать из избранного при нажатии кнопки:
    def makeFavouriteTrack(self):
        sender = self.sender()  # Сигнал
        i = self.buttonFavList.index(sender)  # Находим ID ряда

        # Проверка на то, является ли трек избранным или нет (возвращается булевое значение)
        isFav = self.cursor.execute(f"""SELECT isFav FROM recognized WHERE id={self.id_list[i]}""").fetchone()

        # Если трек уже избран, то удаляем его из избранных:
        if isFav[0]:
            self.cursor.execute(f"""UPDATE recognized
                                    SET isFav = 0
                                    WHERE id={self.id_list[i]}""")

        # Иначе, добавляем в избранное:
        else:
            self.cursor.execute(f"""UPDATE recognized
                                    SET isFav = 1
                                    WHERE id={self.id_list[i]}""")
        self.connect.commit()
        self.update_window()  # Обновляем окно:

    # Удалить трек при нажатии кнопки (Перед этим появляется форма с подтверждением действия):
    def delTrack(self):
        sender = self.sender()  # Сигнал
        i = self.buttonDelList.index(sender)  # Находим ID ряда

        # Форма для выбора страны:
        non_used, ok_pressed = InputDialog().getText(self, 'Удаление', 'Подтвердить удаление?')

        # Если подтверждено удаление:
        if ok_pressed:
            # Выполнение удаления из таблицы:
            if self.is_chart_list[i]:
                self.cursor.execute(f'''DELETE from charts WHERE id={self.id_list[i]}''')
            else:
                self.cursor.execute(f'''DELETE from recognized WHERE id={self.id_list[i]}''')

            # Подтверждение действия:
            self.connect.commit()

            # Удаляем все данные об конкретном ряде:
            del self.id_list[i]
            del self.buttonDelList[i]
            if not self.is_chart_list[i]:  # Удаляем кнопку "избранное", если она существует у ряда:
                del self.buttonFavList[i]
            del self.is_chart_list[i]

            self.update_window()  # Обновляем окно:

    # Очищаем все данные каждого ряда (про id и кнопки):
    def create_new_list(self):
        self.buttonFavList.clear()
        self.buttonDelList.clear()
        self.id_list.clear()
        self.is_chart_list.clear()

    # SQLITE - получаем данные из базы данных:
    def update_db(self, command="""SELECT * FROM recognized"""):
        self.connect = sqlite3.connect('recognized.db')
        self.cursor = self.connect.cursor()

        self.database = self.cursor.execute(command).fetchall()[::-1]
        self.images = [row[2] for row in self.database]

    # Функция для обновления окна:
    def update_window(self):
        if self.table == 'R':
            self.showAllRecognizedTracks()
        elif self.table == 'F':
            self.showAllFavouritesTracks()
        else:
            self.showAllFoundCharts()

    # При закрытии окна, отображаем основное окно:
    def closeEvent(self, event):
        self.close()
        self.main = PyJam()
        self.main.show()


# Lauch the app!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyJam()
    ex.show()
    sys.exit(app.exec())
