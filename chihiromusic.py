import tkinter as tk
from PIL import Image, ImageTk
import requests
import io
from artists_data import artists_data

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chihiro's artist recommendation")
        self.root.geometry("1100x800")  # Set the initial size of the window
        self.root.resizable(False, False)  # Make the window non-resizable

        # List of image paths (replace with your image paths)
        self.image_paths = [
            "beabadoobee.png",
            "bon iver.png",
            "angus and julia stone.png",
            "bright eyes.png",
            "clairo.png",
            "girl in red.png",
            "gregory alan isakov.png",
            "iron and wine.png",
            "jose gonzalez.png",
            "lana del ray.png",
            "mitski.png",
            "rex orange county.png",
            "sufjan stevens.png",
            "the velvet underground.png",
            "alex g.png",
            # ... add paths for all 15 images
        ]

        # Load and resize the background image
        background_image_path = "first frame.png"  # Replace with the path to your image
        original_image = Image.open(background_image_path)
        resized_image = original_image.resize((1100, 800), resample=Image.BICUBIC)
        self.background_photo = ImageTk.PhotoImage(resized_image)

        # Display the resized background image
        self.label_background = tk.Label(root, image=self.background_photo)
        self.label_background.image = self.background_photo
        self.label_background.place(x=0, y=0, relwidth=1, relheight=1)

        # Create and display image buttons in a grid
        self.create_image_buttons()

        # Entry box for artist name
        self.entry_artist = tk.Entry(root, font=("Helvetica", 16), width=60)
        self.entry_artist.place(relx=0.6, rely=0.80, anchor=tk.CENTER)

        # Bind the Enter key to fetch artist details
        self.entry_artist.bind("<Return>", lambda event: self.fetch_artist_details())

        # Quit button
        button_quit = tk.Button(root, text="Quit", command=root.destroy, bg="red", fg="white")
        button_quit.place(relx=0.8, rely=0.7, anchor=tk.S)

    def button_click(self, index):
        def on_image_button_click():
            # Get the artist name based on the selected button index
            artist_names = [
                "Beabadoobee", "Bon Iver", "Angus & Julia Stone", "Bright Eyes", "Clairo",
                "Girl in Red", "Gregory Alan Isakov", "Iron & Wine", "José González",
                "Lana Del Rey", "Mitski", "Rex Orange County", "Sufjan Stevens",
                "The Velvet Underground", "Alex G"
            ]

            if 0 <= index < len(artist_names):
                artist_name = artist_names[index]
                self.show_artist_details(artist_name)

        on_image_button_click()

    def create_image_buttons(self):
        # Create buttons with unique images in a 3x5 grid
        for i in range(3):  # Rows
            for j in range(5):  # Columns
                index = i * 5 + j
                if index < len(self.image_paths):
                    image_path = self.image_paths[index]
                    image = Image.open(image_path)
                    # Resize the image to fit the button size (adjust as needed)
                    image = image.resize((100, 100))
                    photo = ImageTk.PhotoImage(image)

                    button = tk.Button(self.root, image=photo, text=f"Button {index + 1}")
                    button.image = photo  # Keep a reference to the PhotoImage object
                    button.place(x=j * 120 + 150, y=i * 120 + 150)  # Adjust the position as needed

                    # Bind the click event to the button
                    button.bind("<Button-1>", lambda event, idx=index: self.button_click(idx))

    def show_artist_details(self, artist_name):
        # Create a new window for displaying artist details
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Details for {artist_name}")
        
        # Change the background color of the window (replace "lightblue" with your desired color)
        details_window.configure(bg="#FFE6A6")

        # Convert the input artist name to lowercase
        artist_name_lower = artist_name.lower()

        # Check if the artist name is in your local database
        for artist in artists_data:
            if artist['strArtist'].lower() == artist_name_lower:
                # Display the artist image
                image_url = artist['strArtistFanart']
                image_data = requests.get(image_url).content
                image = Image.open(io.BytesIO(image_data))

                # Resize the image
                photo_size = (500, 500)
                image.thumbnail(photo_size)

                photo = ImageTk.PhotoImage(image)
                label_image = tk.Label(details_window, image=photo)
                label_image.image = photo  # Keep a reference to the PhotoImage object
                label_image.grid(row=0, column=0, pady=10)  # ... (existing code)

                # Display the artist details below the image
                details_text = f"Artist Name: {artist['strArtist']}\n"
                details_text += f"Genre: {artist['strGenre']}\n"
                details_text += f"Formed Year: {artist['intFormedYear']}\n"
                details_text += f"Biography: {artist['strBiographyEN']}"

                text_widget = tk.Text(details_window, height=10, width=150, wrap=tk.WORD)
                text_widget.insert(tk.END, details_text)

                # Configure font and formatting
                text_widget.tag_configure("bold", font=("Helvetica", 12, "bold"))
                text_widget.tag_configure("normal", font=("Helvetica", 12,))

                # Apply formatting to specific parts of the text
                text_widget.tag_add("bold", "1.0", "1.13")  # Assuming "Artist Name:" is 13 characters long
                text_widget.tag_add("bold", "2.0", "2.5")   # Assuming "Genre:" is 5 characters long
                text_widget.tag_add("bold", "3.0", "3.12")  # Assuming "Formed Year:" is 12 characters long
                text_widget.tag_add("bold", "4.0", "4.11")  # Rest of the text

                text_widget.config(state=tk.DISABLED)  # Make the text widget read-only
                text_widget.grid(row=1, column=0, pady=5)

                # Add a "Back" button to close the details window
                back_button = tk.Button(details_window, text="Back", command=details_window.destroy)
                back_button.grid(row=2, column=0, pady=10)

                break
        else:
            # If artist not found, show a message in the details window
            label_error = tk.Label(details_window, text=f"Artist '{artist_name}' not found in the local database")
            label_error.grid(row=2, column=0, pady=10)

    def fetch_artist_details(self):
        # Get the artist name from the entry box
        artist_name = self.entry_artist.get().strip()

        if not artist_name:
            return

        # Fetch and display artist details
        self.show_artist_details(artist_name)

    def back_to_entry(self):
        # Clear previous widgets in the grid
        for widget in self.root.grid_slaves():
            widget.grid_forget()

        # Recreate and display image buttons
        self.create_image_buttons()


if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
