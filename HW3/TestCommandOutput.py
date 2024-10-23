import unittest
import subprocess
import time
import os

def check_command_output(command, search_text):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0 and search_text in result.stdout
    except Exception:
        return False

class TestCommandOutput(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создаем файл для статистики, если его еще нет
        with open("stat.txt", "w") as f:
            f.write("")

    def add_statistics(self, file_count, file_size):
        load_stats = open("/proc/loadavg").read()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        with open("stat.txt", "a") as f:
            f.write(f"{current_time}, {file_count}, {file_size}, {load_stats}\n")

    def test_list_directory_files(self):
        # Пример: Проверка наличия определенного файла в текущем каталоге
        file_to_search = "README.md"  # Замените на ваше имя файла
        result = check_command_output("ls", file_to_search)
        self.assertTrue(result, f"Файл '{file_to_search}' не найден в выводе команды 'ls'.")
        
        # Получаем количество файлов и размер файла
        file_count = len(os.listdir('.'))
        file_size = os.path.getsize(file_to_search) if os.path.exists(file_to_search) else 0
        self.add_statistics(file_count, file_size)

    def test_extract_archive(self):
        # Создаем тестовый архив для проверки
        archive_name = "test_archive.tar.gz"
        with open("test_file.txt", "w") as f:
            f.write("Test content")
        subprocess.run(f"tar -czf {archive_name} test_file.txt", shell=True)

        # Проверяем разархивирование
        extract_result = check_command_output(f"tar -xzf {archive_name} && ls", "test_file.txt")
        self.assertTrue(extract_result, "Файл 'test_file.txt' не найден после разархивирования.")

        # Получаем количество файлов и размер файла
        file_count = len(os.listdir('.'))
        file_size = os.path.getsize("test_file.txt")
        self.add_statistics(file_count, file_size)

        # Удаляем тестовые файлы
        subprocess.run(f"rm {archive_name} test_file.txt", shell=True)

    @classmethod
    def tearDownClass(cls):
        # После всех тестов можно удалить файл статистики, если нужно
        if os.path.exists("stat.txt"):
            os.remove("stat.txt")


if __name__ == "__main__":
    unittest.main()