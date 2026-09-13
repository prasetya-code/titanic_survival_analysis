## Overview

Data telah dibagi menjadi dua kelompok:

* **Training set (`train.csv`)**: Digunakan untuk membangun model *machine learning*. Pada file ini, hasil (dikenal juga sebagai *"ground truth"*) untuk setiap penumpang telah disediakan. Model Anda akan dibuat berdasarkan fitur-fitur seperti jenis kelamin dan kelas penumpang. Anda juga dapat menggunakan *feature engineering* untuk membuat fitur baru.
* **Test set (`test.csv`)**: Digunakan untuk menguji seberapa baik kinerja model Anda pada data baru (*unseen data*). Pada file ini, *ground truth* tidak disediakan. Tugas Anda adalah memprediksi apakah setiap penumpang di *test set* selamat atau tidak dari tenggelamnya kapal Titanic.
* **`gender_submission.csv`**: Contoh file pengiriman (*submission*) yang mengasumsikan hanya penumpang perempuan yang selamat.

---

## Data Dictionary

| Variable | Definition | Key |
| :--- | :--- | :--- |
| **survival** | Survival | `0` = No, `1` = Yes |
| **pclass** | Ticket class | `1` = 1st (Upper), `2` = 2nd (Middle), `3` = 3rd (Lower) |
| **sex** | Sex | — |
| **Age** | Age in years | — |
| **sibsp** | # of siblings / spouses aboard the Titanic | — |
| **parch** | # of parents / children aboard the Titanic | — |
| **ticket** | Ticket number | — |
| **fare** | Passenger fare | — |
| **cabin** | Cabin number | — |
| **embarked** | Port of Embarkation | `C` = Cherbourg, `Q` = Queenstown, `S` = Southampton |

---

## Variable Notes

* **`pclass`**  
  Representasi dari status sosial-ekonomi (*Socio-Economic Status* / SES):
  * `1st` = Kelas Atas (*Upper*)
  * `2nd` = Kelas Menengah (*Middle*)
  * `3rd` = Kelas Bawah (*Lower*)

* **`age`**  
  Umur berbentuk pecahan jika kurang dari 1 tahun. Jika umur merupakan perkiraan, formatnya berupa `xx.5`.

* **`sibsp`**  
  Hubungan keluarga didefinisikan sebagai berikut:
  * **Sibling** = saudara kandung, saudara tiri (laki-laki/perempuan)
  * **Spouse** = suami, istri (tunangan dan kekasih diabaikan)

* **`parch`**  
  Hubungan keluarga didefinisikan sebagai berikut:
  * **Parent** = ibu, ayah
  * **Child** = anak perempuan, anak laki-laki, anak tiri
  * *Catatan:* Beberapa anak hanya bepergian dengan pengasuh, sehingga untuk mereka `parch = 0`.