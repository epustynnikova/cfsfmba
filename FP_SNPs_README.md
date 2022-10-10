# Скрипт трансформации #

## Предпоготовка данных

### Предпоготовка FP_SNPs.txt
Для корректной работы скрипта необходимо запустить следующие команды:
```shell
./prepare_FP_SNPs.sh
```
### Предпоготовка референса
Для корректной работы скрипта необходимо разархивировать референс, проиндексировать и сделать сплит по хромосомам:
```shell
tar -xvf GRCh38.d1.vd1.fa.tar.gz
faidx --split-files GRCh38.d1.vd1.fa
```
Для локальной проверки достаточно скачать [референс](http://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/GetZip.cgi?zip_name=GRAF_files.zip), положить его в папку data/ и запустить ./prepare_GRCh38.sh (хоть это и займёт некоторое время).
## Скрипт
### Аргументы скрипта
* -i --input входной файл (по умолчанию data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv)
* -o --output выходной файл (по умолчанию data/FP_SNPs_output.tsv)
* -r --reference директория с проиндексированным референсом (по умолчанию data/ref/)
### Статусы поиска в референса
* NOT_FOUND_REF -- не наден файл с референсной хромосомой
* NOT_FOUND_OUT_OF_RANGE -- ошибка при поиске: pysam.Fastafile -- if the coordinates are out of range
* NOT_FOUND_REGION_IS_INVALID -- ошибка при поиске pysam.Fastafile -- if the region is invalid
### Пример запуска
```shell
python scripts/transform.py -i data/FP_SNPs_10k_GB38_twoAllelsFormat.tsv -o data/FP_SNPs_output.tsv -r data/ref/
```
## Разработка
## Установить pre-commit-hooks
```shell
pre-commit install
```
### Запустить тесты
```shell
./run_test.sh
```
### Собрать wheel
```shell
./run_wheel.sh
```
Расположение файла после выполнения команды: dist/cfsfmba-1.0.0-py3-none-any.whl
