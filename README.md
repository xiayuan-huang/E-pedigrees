
# E-pedigrees

E-pdigrees combines two validated family prediction algorithms (FPPA and RIFTEHR) into a single software package for high throughput pedigrees construction. The convenient software considers patients’ basic demographic information and/or emergency contact data to infer high-accuracy parent-child relationship. Importantly, E-Pedigrees allows users to layer in additional pedigree data when available and provides options for applying different logical rules to improve accuracy of inferred family relationships. You can refer to two papers for the details of two core algorithms. ["Applying family analyses to electronic health
records to facilitate genetic research"](https://academic.oup.com/bioinformatics/article/34/4/635/4158031) and ["Disease Heritability Inferred from Familial Relationships Reported in Medical Records"](https://www.cell.com/cell/pdf/S0092-8674(18)30525-7.pdf).



## Input and output requirements:

Run main.py with required input files and correct format.

Our code is compatible with most format of Electronic Health Records system, you can provide options of de-identified files as inputs:
1. Basic demographic information:
   - Address file
   - Name file
   - Demographic file
   - Account file
2. Self-reported relationship data:
   - Patient file
   - Emergency contact file
3. Family pedigree file in standard PED format:
   - pedigree file
  

### Address file

The address file is a csv comma delimited file containing eight columns: **study_id**, **street_1**, **street_2**, **city**, **state**, **zip**, **from_year** and **thru_year**. The **study_id** is the de-identified id for a single patient. The **street_1**, **street_2**, **city**, **state** and **zip** are the de-identified address. The **from_year** and **thru_year** shows from which year through which year this patient lived in this address. Note that all missing information will be shown as blank.


| study_id      | street_1      | street_2  | city   | state   | zip   | from_year   | thru_year   |
| ------------- |:-------------:| ---------:| ------:|--------:|------:|------------:|------------:|
| 1             | 790393        |           | 7200   | 28      | 18216 |             |             |
| 10            | 117141        |           | 5115   | 28      | 11753 |             | 2005        |
| 56            | 221591        | 448275    | 2893   | 28      | 9427  | 2003        | 2011        |


### Name file

The name file is a csv comma delimited file containing six columns: **study_id**, **last_name_id**, **first_name_id**, **middle_name_id**, **from_year** and **thru_year**. The **study_id** is the de-identified id for a single patient. The **last_name_id**, **first_name_id** and **middle_name_id** are the de-identified names. The **from_year** and **thru_year** shows from which year through which year this patient used this name. Note that all missing information will be shown as blank.


| study_id | last_name_id   | first_name_id  | middle_name_id   | from_year   | thru_year   |
| ---------|:--------------:| --------------:| ----------------:|------------:|------------:|
| 1        | 103775         | 53806          |                  |             |             |
| 10       | 46972          | 44623          |                  | 2005        | 2011        |
| 50       | 2696           | 62099          |                  | 1997        | 2007        |
| 50       | 105616         | 62099          |                  |             | 1997        |


### Demographic file

The demographic file is a csv comma delimited file containing seven columns: **study_id**, **gender_code**, **birth_year**, **deceased_year**, **PHONE_NUM_id**, **from_year** and **thru_year**. The **study_id** is the de-identified id for a single patient. The **gender_code** is "F" for female, "M" for male, "U" for unknown and blank for missing value.

| study_id | gender_code   | birth_year  | deceased_year   | PHONE_NUM_id   | from_year   | thru_year   |
| -------- |:-------------:| -----------:| ---------------:|---------------:|------------:|------------:|
| 1        | F             | 1989        |                 |                |             |             |
| 2        | F             | 1947        |                 | 134271         |             | 2011        |
| 282056   | U             | 1986        | 2010            |                |             |             |


### Account file
 
The account file is a csv comma delimited file containing four columns: **study_id**, **ACCT_NUM_id**, **from_year** and **thru_year**. The **study_id** is the de-identified id for a single patient. The **ACCT_NUM_id** is the de-identified id for account. Note that all missing information will be shown as blank.

| study_id | ACCT_NUM_id   | from_year   | thru_year   |
| -------- |--------------:|------------:|------------:|
| 2        | 982162        |             | 2011        |
| 10       | 523063        | 2005        | 2011        |


### Patient file

The patient file is a csv comma delimited file containing five columns: **study_id**, **first_name_id**, **last_name_id**, **PHONE_NUM_id** and **zip**.

| PatientID|  FirstName     |    LastName    |       Sex        |  PhoneNumber    |   Zipcode   |  birth_year | deceased_year |
| ---------|:--------------:| --------------:|-----------------:|----------------:|------------:|------------:|--------------:|
| 1        | 103775         | 53806          |         M        |   1112223333    |    18216    |     1970    |               |  
| 10       | 46972          | 44623          |         M        |   2223334444    |    11753    |     1972    |               |  
| 50       | 2696           | 62099          |         F        |   3334445555    |    18216    |     1980    |               |
| 96       | 105616         | 53806          |         F        |   1112223333    |    10032    |     1956    |               |
| 122      | 345228         | 44623          |         F        |   2223334444    |    11753    |     1990    |               |


### Emergency contact file

The emergency contact file is a csv comma delimited file containing six columns: **study_id**, **EC_FirstName**, **EC_LastName**, **EC_PhoneNumber**, **EC_Zipcode** and **EC_Relationship**. Columns two to five are the information of emergency contact person to the patient. **study_id** is the identity ID of the patient. **EC_Relationship** is the self-reported relationship of emergency contact person to the patient. e.g. "Mother" means the emergency contact person is the mother of the patient.

| PatientID| EC_FirstName   | EC_LastName    | EC_PhoneNumber   | EC_Zipcode  | EC_Relationship  |
| ---------|:--------------:| --------------:| ----------------:|------------:|-----------------:|
| 1        | 105616         | 53806          |     1112223333   |    18216    |      Mother      |
| 10       | 345228         | 44623          |     2223334444   |    11753    |      Father      |


### Pedigree file

| family_ID | num_fam_member | individual_ID  |   Maternal ID    | Paternal_ID |    Gender   |
| --------- |:--------------:| --------------:| ----------------:|------------:|------------:|
| 1         |        5       |      50        |     1112223333   |    18216    |      M      |
| 2         |        3       |      96        |     2223334444   |    11753    |      F      |


### Output files

Eventually we will get one output files: 1. parent_child relathionship file and pedigree file.
The parent_child relationship file is an intermediate txt file which records the predicted parent_child relationship between a pair of patients. The pedigree file is the final output family pedigrees csv file in standard PED format which contains six colums: 1. randomly assgined family ID, 2. number of family members, 3. patient's de-identified study id, 4. this patient's mother's de-identified study id, 5. this patient's father's de-identified study id and 6. gender code of this patient.


## Running E-pedigrees:
Please refer to the user manual.
