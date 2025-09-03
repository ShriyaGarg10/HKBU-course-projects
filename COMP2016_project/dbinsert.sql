
CREATE TABLE Books (
	Call_no CHAR(5) PRIMARY KEY,
	ISBN CHAR(13) UNIQUE NOT NULL,
	Title VARCHAR(50) NOT NULL,
	Author VARCHAR(20) NOT NULL,
	Amount INTEGER NOT NULL,
	CHECK (Amount >= 0),
	Location VARCHAR(10) NOT NULL
);


CREATE TABLE Students (
	St_no CHAR(8) PRIMARY KEY,
	Name VARCHAR(20) NOT NULL,
	Gender CHAR(1) CHECK (Gender IN ('M', 'F','O')),
	Major VARCHAR(10) NOT NULL
);


CREATE TABLE BorrowRecords (
	Borrower CHAR(8) REFERENCES Students(St_no),
	Book CHAR(5) REFERENCES Books(Call_no),
	BorrowDate DATE NOT NULL,
	DueDate DATE NOT NULL,
	CHECK (DueDate > BorrowDate),
	PRIMARY KEY (Borrower, Book)
);


-- Create Renewals table
CREATE TABLE Renewals (
    Student CHAR(8) REFERENCES Students(St_no),
    RenewedBook CHAR(5) REFERENCES Books(Call_no),
    PRIMARY KEY (Student, RenewedBook)
);


--Each student can reserve only one book
CREATE TABLE Reservations (
    Student CHAR(8) REFERENCES Students(St_no),
    ReservedBook CHAR(5) REFERENCES Books(Call_no),
    RequestDate DATE NOT NULL,
    PRIMARY KEY (Student)
);



-- Insert sample data into Students table
INSERT INTO Students VALUES ('12345678', 'A', 'M', 'Comp');
INSERT INTO Students VALUES ('11111111', 'B', 'M', 'Math');
INSERT INTO Students VALUES ('22222222', 'C', 'F', 'COMM');
INSERT INTO Students VALUES ('33333333', 'D', 'F', 'COMM');
INSERT INTO Students VALUES ('44444444', 'E', 'M', 'Comp');
INSERT INTO Students VALUES ('55555555', 'F', 'M', 'COMM');
INSERT INTO Students VALUES ('66666666', 'G', 'F', 'Math');
INSERT INTO Students VALUES ('77777777', 'H', 'M', 'Comp');

-- Insert sample data into Books table
INSERT INTO Books VALUES ('A0000', '0-306-40615-1', 'AA', 'XX', 0, 'S1E01');
INSERT INTO Books VALUES ('B0000', '0-306-40615-2', 'BB', 'YY', 0, 'S2E02');
INSERT INTO Books VALUES ('C1111', '0-306-40615-3', 'CC', 'ZZ', 2, 'D1E11');
INSERT INTO Books VALUES ('B0001', '0-306-40615-4', 'DD', 'UU', 2, 'G1E00');
INSERT INTO Books VALUES ('A1111', '0-306-40615-5', 'EE', 'VV', 2, 'B1E00');
INSERT INTO Books VALUES ('D0101', '0-306-40615-6', 'FF', 'WW', 1, 'B2E11');
INSERT INTO Books VALUES ('E0000', '0-306-40615-7', 'GG', 'PP', 0, 'X0E22');
INSERT INTO Books VALUES ('E0100', '0-306-40615-8', 'HH', 'QQ', 2, 'X0E21');
INSERT INTO Books VALUES ('E0111', '0-306-40615-9', 'II', 'RR', 0, 'X0E44');


INSERT INTO BorrowRecords VALUES ('11111111', 'D0101', TO_DATE('24-Mar-2025', 'DD-Mon-YYYY'), TO_DATE('21-Apr-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('55555555', 'A1111', TO_DATE('23-Mar-2025', 'DD-Mon-YYYY'), TO_DATE('20-Apr-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('22222222', 'B0000', TO_DATE('31-Mar-2025', 'DD-Mon-YYYY'), TO_DATE('12-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('11111111', 'A0000', TO_DATE('1-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('29-Apr-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('33333333', 'A0000', TO_DATE('3-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('1-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('11111111', 'B0000', TO_DATE('3-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('15-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('44444444', 'C1111', TO_DATE('4-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('16-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('44444444', 'A0000', TO_DATE('6-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('4-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('33333333', 'C1111', TO_DATE('6-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('4-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('33333333', 'A1111', TO_DATE('6-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('4-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('33333333', 'B0001', TO_DATE('6-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('4-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('44444444', 'D0101', TO_DATE('10-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('8-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('33333333', 'D0101', TO_DATE('10-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('8-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('44444444', 'A1111', TO_DATE('14-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('12-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('55555555', 'C1111', TO_DATE('18-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('16-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('22222222', 'E0111', TO_DATE('19-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('17-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('11111111', 'E0000', TO_DATE('20-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('18-May-2025', 'DD-Mon-YYYY'));
INSERT INTO BorrowRecords VALUES ('44444444', 'B0001', TO_DATE('21-Apr-2025', 'DD-Mon-YYYY'), TO_DATE('19-May-2025', 'DD-Mon-YYYY'));



INSERT INTO Reservations  VALUES ('12345678', 'A0000', TO_DATE('20-Apr-2025', 'DD-Mon-YYYY'));
INSERT INTO Reservations  VALUES ('66666666', 'E0000', TO_DATE('22-Apr-2025', 'DD-Mon-YYYY'));


INSERT INTO Renewals VALUES ('22222222', 'B0000');
INSERT INTO Renewals VALUES ('11111111', 'B0000');
INSERT INTO Renewals VALUES ('44444444', 'C1111');



--Trigger to set DueDate by default
CREATE OR REPLACE TRIGGER SetDueDate
BEFORE INSERT ON BorrowRecords
FOR EACH ROW
BEGIN
    :NEW.DueDate := :NEW.BorrowDate + 28;
END;
/

-- Create Trigger for Book Borrow/Return Updates
CREATE OR REPLACE TRIGGER UpdateBookAmountOnBorrow
AFTER INSERT ON BorrowRecords
FOR EACH ROW
BEGIN
    UPDATE Books 
    SET Amount = Amount - 1 
    WHERE Call_no = :NEW.Book;
END;
/

CREATE OR REPLACE TRIGGER UpdateBookAmountOnReturn
AFTER DELETE ON BorrowRecords
FOR EACH ROW
BEGIN
    UPDATE Books 
    SET Amount = Amount + 1 
    WHERE Call_no = :OLD.Book;
END;
/

--TESTING(UNCOMMENT FOR TESTING THE TRIGGERS)
--SELECT Call_no, Amount FROM Books WHERE Call_no = 'D0101';
--Displays the original amount of book D0101

--INSERT INTO BorrowRecords VALUES ('66666666', 'D0101', TO_DATE('25-Apr-2025', 'DD-Mon-YYYY'), DEFAULT);
--SELECT BorrowDate, DueDate FROM BorrowRecords WHERE Borrower = '66666666' AND Book = 'D0101';
--This should have the Due date as Borrowed date + 28 days

--SELECT Call_no, Amount FROM Books WHERE Call_no = 'D0101';
--Amount should have now reduced by 1

--DELETE FROM BorrowRecords WHERE Borrower = '66666666' AND Book = 'D0101';
--SELECT Call_no, Amount FROM Books WHERE Call_no = 'D0101';
--Amount should now have increased by 1



