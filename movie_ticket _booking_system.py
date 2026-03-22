import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class movies():
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Reservation")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Movie Ticket Reservation", bd=4, relief="raised",
                        fg="orange", bg="gray", font=("Arial", 50, "bold"))
        title.pack(side="top", fill="x")

        # Initialize database
        self.initDB()

        # Frame
        self.frame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(250, 150, 150))
        self.frame.place(width=self.width-300, height=self.height-180, x=150, y=100)

        optLbl = tk.Label(self.frame, text="Select_Show:", bg=self.clr(250, 150, 150),
                         fg="white", font=("Arial", 15, "bold"))
        optLbl.grid(row=0, column=0, padx=20, pady=30)
        self.opt = ttk.Combobox(self.frame, font=("Arial", 15, "bold"),
                               values=("First", "Second", "Third"), width=17)
        self.opt.set("Select_One")
        self.opt.grid(row=0, column=1, padx=10, pady=30)

        nameLbl = tk.Label(self.frame, text="Your_Name:", bg=self.clr(250, 150, 150),
                          fg="white", font=("Arial", 15, "bold"))
        nameLbl.grid(row=0, column=2, padx=20, pady=30)
        self.name = tk.Entry(self.frame, bd=3, width=18, font=("Arial", 15, "bold"))
        self.name.grid(row=0, column=3, padx=10, pady=30)

        okBtn = tk.Button(self.frame, command=self.reserveFun, text="Reserve",
                         font=("Arial", 15, "bold"), width=8)
        okBtn.grid(row=0, column=4, padx=30, pady=30)

        self.tabFun()
        self.bookingTabFun()

    def initDB(self):
        """Initialize database and tables if they don't exist"""
        try:
            # Connect without database first
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Nitesh@1914',
                auth_plugin='mysql_native_password'
            )
            cur = con.cursor()
            
            # Create database if not exists
            cur.execute("CREATE DATABASE IF NOT EXISTS rec")
            con.commit()
            con.close()
            
            # Now connect to the rec database
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Nitesh@1914',
                database='rec',
                auth_plugin='mysql_native_password'
            )
            cur = con.cursor()
            
            # Create movie table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS movie (
                    show_no VARCHAR(20) PRIMARY KEY,
                    show_time VARCHAR(50),
                    movie_name VARCHAR(100),
                    price INT,
                    seats INT
                )
            """)
            
            # Create bookings table to track seat allocations
            cur.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    show_no VARCHAR(20),
                    customer_name VARCHAR(100),
                    row_no INT,
                    seat_no INT,
                    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (show_no) REFERENCES movie(show_no)
                )
            """)
            
            # Check if movie table has data, if not insert sample data
            cur.execute("SELECT COUNT(*) FROM movie")
            count = cur.fetchone()[0]
            
            if count == 0:
                sample_data = [
                    ('First', '10:00 AM - 1:00 PM', 'Avengers: Endgame', 15, 20),
                    ('Second', '2:00 PM - 5:00 PM', 'The Dark Knight', 12, 20),
                    ('Third', '6:00 PM - 9:00 PM', 'Inception', 18, 20)
                ]
                cur.executemany("""
                    INSERT INTO movie (show_no, show_time, movie_name, price, seats)
                    VALUES (%s, %s, %s, %s, %s)
                """, sample_data)
            
            con.commit()
            con.close()
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Error initializing database: {e}")

    def tabFun(self):
        """Create table for showing movie details"""
        tabFrame = tk.Frame(self.frame, bd=5, relief="sunken", bg=self.clr(150, 150, 150))
        tabFrame.place(width=self.width-400, height=300, x=50, y=90)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("showNo", "time", "movie", "price", "seats"))
        
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("showNo", text="Show_No")
        self.table.heading("time", text="Time_Table")
        self.table.heading("movie", text="Movie_Name")
        self.table.heading("price", text="Price")
        self.table.heading("seats", text="Available_Seats")
        self.table["show"] = "headings"

        self.table.column("showNo", width=200)
        self.table.column("time", width=200)
        self.table.column("movie", width=200)
        self.table.column("price", width=80)
        self.table.column("seats", width=80)
        
        self.table.pack(fill="both", expand=1)

        self.showFun()

    def bookingTabFun(self):
        """Create table for showing booking details"""
        bookFrame = tk.Frame(self.frame, bd=5, relief="sunken", bg=self.clr(150, 150, 150))
        bookFrame.place(width=self.width-400, height=self.height-620, x=50, y=410)

        bookLbl = tk.Label(self.frame, text="Booking Details:", bg=self.clr(250, 150, 150),
                          fg="white", font=("Arial", 15, "bold"))
        bookLbl.place(x=50, y=375)

        x_scrol = tk.Scrollbar(bookFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(bookFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.bookTable = ttk.Treeview(bookFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                      columns=("id", "showNo", "name", "row", "seat", "time"))
        
        x_scrol.config(command=self.bookTable.xview)
        y_scrol.config(command=self.bookTable.yview)
        
        self.bookTable.heading("id", text="Booking_ID")
        self.bookTable.heading("showNo", text="Show_No")
        self.bookTable.heading("name", text="Customer_Name")
        self.bookTable.heading("row", text="Row_No")
        self.bookTable.heading("seat", text="Seat_No")
        self.bookTable.heading("time", text="Booking_Time")
        self.bookTable["show"] = "headings"

        self.bookTable.column("id", width=100)
        self.bookTable.column("showNo", width=100)
        self.bookTable.column("name", width=200)
        self.bookTable.column("row", width=80)
        self.bookTable.column("seat", width=80)
        self.bookTable.column("time", width=180)
        
        self.bookTable.pack(fill="both", expand=1)

        self.showBookings()

    def showFun(self):
        """Display movie data in table"""
        try:
            self.dbFun()
            self.cur.execute("SELECT * FROM movie")
            data = self.cur.fetchall()

            self.table.delete(*self.table.get_children())
            for i in data:
                self.table.insert('', tk.END, values=i)

            self.con.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def showBookings(self):
        """Display booking data in table"""
        try:
            self.dbFun()
            self.cur.execute("SELECT * FROM bookings ORDER BY booking_time DESC")
            data = self.cur.fetchall()

            self.bookTable.delete(*self.bookTable.get_children())
            for i in data:
                self.bookTable.insert('', tk.END, values=i)

            self.con.close()

        except Exception as e:
            messagebox.showerror("Error", f"Error loading bookings: {e}")

    def reserveFun(self):
        """Reserve a seat for customer"""
        opt = self.opt.get()
        name = self.name.get()
        
        if opt and name and opt != "Select_One":
            try:
                self.dbFun()
                self.cur.execute("""
                    SELECT show_time, movie_name, price, seats 
                    FROM movie WHERE show_no = %s
                """, (opt,))
                row = self.cur.fetchone()
                
                if row and row[3] > 0:
                    # Get count of already booked seats for this show
                    self.cur.execute("""
                        SELECT COUNT(*) FROM bookings WHERE show_no = %s
                    """, (opt,))
                    booked_count = self.cur.fetchone()[0]
                    
                    # Calculate row and seat number based on booked count
                    row_no = (booked_count // 5) + 1
                    seat_no = (booked_count % 5) + 1
                    
                    # Update available seats
                    upd = row[3] - 1
                    self.cur.execute("UPDATE movie SET seats=%s WHERE show_no=%s", (upd, opt))
                    
                    # Insert booking record
                    self.cur.execute("""
                        INSERT INTO bookings (show_no, customer_name, row_no, seat_no)
                        VALUES (%s, %s, %s, %s)
                    """, (opt, name, row_no, seat_no))
                    
                    self.con.commit()
                    
                    messagebox.showinfo("Success", 
                        f"Booking Confirmed!\n\n"
                        f"Customer: {name}\n"
                        f"Show: {opt}\n"
                        f"Movie: {row[1]}\n"
                        f"Row: {row_no}\n"
                        f"Seat: {seat_no}\n"
                        f"Amount to Pay: ${row[2]}\n\n"
                        f"Available Seats: {upd}")
                    
                    # Refresh both tables
                    self.showFun()
                    self.showBookings()
                    
                    # Clear input fields
                    self.name.delete(0, tk.END)
                    self.opt.set("Select_One")
                    
                else:
                    messagebox.showerror("Error", "All Seats Reserved for this Show")
                    
                self.con.close()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")
        else:
            messagebox.showerror("Error", "Please Fill All Input Fields!")

    def dbFun(self):
        """Connect to database"""
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Nitesh@1914",
            database="rec",
            auth_plugin='mysql_native_password'
        )
        self.cur = self.con.cursor()

    def clr(self, r, g, b):
        """Convert RGB to hex color"""
        return f"#{r:02x}{g:02x}{b:02x}"


if __name__ == "__main__":
    root = tk.Tk()
    obj = movies(root)
    root.mainloop()