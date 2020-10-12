
create table medicine_master(medicine_id int(11) AUTO_INCREMENT PRIMARY KEY, medicine_nm varchar(50), qty_available int(11), rate double(11,3));

insert into medicine_master values(1,'Atenolol', 95, 200),(2,'Acebutolol', 120, 550),(3,'Corgard', 100, 2000),(4, 'Tenormin', 125, 100),(5, 'Bactrim', 135, 90);

insert into medicine_master values(6, 'Bentyl', 115, 120),(7, 'Clozapin', 130, 105),(8, 'Dexilant', 145, 80),(9, 'Ditropan', 100, 500),(10, 'Norflex', 140, 200);

desc medicine_master;

select * from medicine_master;


create table track_medicines(pid int references patients(pid), medicine_id int(11) references medicine_master(medicine_id), qty_issued int(11));

insert into track_medicines values(1, 1, 10),(1, 3, 5);

insert into track_medicines values(1, 6, 2),(3, 4, 3);

desc track_medicines;

select * from track_medicines;

create table patient(patient_id int(10) PRIMARY KEY, patient_nm varchar(50), addr varchar(200), age int(3), doj date, room_type varchar(8));

insert into patient values(1234, 'Joseph', 'Rick Street, Ameerrtpet, Hyderabad', 56, '2020-07-02', 'Single');

insert into patient values(1235, 'Ahmed', 'James Street, RP Road, Hyderabad', 65, '2020-06-25', 'Shared');

insert into patient values(1236, 'Nirnay', 'Doyen Street, Nedhry Nagar, Hyderabad', 76, '2020-06-28', 'General');

insert into patient values(1237, 'Sonia', 'Park Lane, Begumpet, Hyderabad', 66, '2020-06-30', 'Single');

insert into patient values(1238, 'Rahul', 'Nehru Street, Gandhinagar, Hyderabad', 46, '2020-06-23', 'General');

desc patient;

select * from patient;

create table diagnostics_master(test_id int(11) auto_increment primary key, test_nm varchar(50), charges double(15,3));

insert into diagnostics_master values(1, 'Biopsy', 35000),(2, 'Colonoscopy', 31500),(3, 'CT', 42000),(4, 'ECG', 300),(5, 'Echo', 17500),(6, 'CBP', 10500),(7, 'Lipid', 1400),(8, 'MRI', 40250);

desc diagnostics_master;

select * from diagnostics_master;


create table track_diagnostics(pid int, test_id int(11), foreign key(pid) references patients(pid), foreign key(test_id) references diagnostics_master(test_id));

insert into track_diagnostics(pid,test_id) values(1,6);

insert into track_diagnostics values(1,5),(1,7);

desc track_diagnostics;

select * from track_diagnostics;

create table executive(login varchar(20),password varchar(10));

insert into executive(login,password) values('Execu0001','Execu@0001'),('Execu0002','Execu@0002');

desc executive;

select * from executive;

create table pharmacist(login varchar(20),password varchar(10));

insert into pharmacist(login,password) values('Pharm0001','Pharm@0001'),('Pharm0002','Pharm@0002');

desc pharmacist;

select * from pharmacist;

create table diagnostic(login varchar(20),password varchar(10));

insert into diagnostic(login,password) values('Diag00001','Diag@00001'),('Diag0002','Diag@00002');

desc diagnostic;

select * from diagnostic;