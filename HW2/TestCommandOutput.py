import unittest
import subprocess

def check_command_output(command, search_text):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0 and search_text in result.stdout
    except Exception:
        return False

class TestCommandOutput(unittest.TestCase):

    def test_list_directory_files(self):
        # Пример: Проверка наличия определенного файла в текущем каталоге
        file_to_search = "README.md"  # Замените на ваше имя файла
        result = check_command_output("ls", file_to_search)
        self.assertTrue(result, f"Файл '{file_to_search}' не найден в выводе команды 'ls'.")

    def test_extract_archive(self):
        # Создаем тестовый архив для проверки
        archive_name = "test_archive.tar.gz"
        with open("test_file.txt", "w") as f:
            f.write("Test content")
        subprocess.run(f"tar -czf {archive_name} test_file.txt", shell=True)

        # Проверяем разархивирование
        extract_result = check_command_output(f"tar -xzf {archive_name} && ls", "test_file.txt")
        self.assertTrue(extract_result, "Файл 'test_file.txt' не найден после разархивирования.")

        # Удаляем тестовые файлы
        subprocess.run(f"rm {archive_name} test_file.txt", shell=True)

if __name__ == "__main__":
    unittest.main()