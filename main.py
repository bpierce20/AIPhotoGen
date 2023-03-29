import openai
import customtkinter
from PIL import Image, ImageTk
from urllib.request import urlopen

openai.api_key = "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"

    
class PhotoClass():
    def __init__(self, photo_prompt, photo_url):
        self.photo_prompt = photo_prompt
        self.photo_url = photo_url      

ai_gen_photo = PhotoClass(photo_prompt="null", photo_url="null")

class prompt_window(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Edit Prompt")
        self.geometry("592x251")
        prompt_textbox = customtkinter.CTkTextbox(self,width=592)
        prompt_textbox.grid(column=0,row=0)

        def save_prompt():
            isSaved = False
            ai_gen_photo.photo_prompt = prompt_textbox.get("0.0", "end")
            isSaved = True
            if(isSaved):
                save_window = customtkinter.CTkToplevel()
                save_window.title("Prompt Saved")
                save_window.geometry("345x83")
                save_label = customtkinter.CTkLabel(save_window,text="Your prompt was saved. You can now generate an image.")
                save_label.grid(column=0,row=0, padx=10,pady=10)
                def close_dialog():
                    save_window.destroy()

               

                okay_button = customtkinter.CTkButton(save_window, text="Okay", command=close_dialog)
                okay_button.grid(column=0, row=1)
               

            
                save_window.grab_set()

            print(ai_gen_photo.photo_prompt)

            
        def get_winsize():
                print("The width is: ", self.winfo_width())
                print("The height is: ", self.winfo_height())
        save_prompt_button = customtkinter.CTkButton(self, text="Save Prompt", command=save_prompt)
        save_prompt_button.grid(column=0,row=1, padx=10, pady=10)
        self.grab_set()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        WIDTH = 710
        HEIGHT = 520

        self.title("AI Photo Generator")
        self.config(bg='#1F2022')
        self.geometry(f'{WIDTH}x{HEIGHT}')


        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame_left = customtkinter.CTkFrame(
            master=self, width=180, corner_radius=0,)
        frame_left.grid(column=0, row=0, sticky="nswe")

        frame_right = customtkinter.CTkFrame(master=self)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.toplevel_window = None

        # Buttons for left frame

        # Method to put image in right frame
        def place_image():
            image_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-T6fKLIpHkTpa10AOJyenlD7u/user-q5PP041Qh1n4zRkGHIEIQwPv/img-gFx78FXkjacj1GkbDNMKLRy2.png?st=2023-02-06T09%3A01%3A17Z&se=2023-02-06T11%3A01%3A17Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-02-06T04%3A38%3A20Z&ske=2023-02-07T04%3A38%3A20Z&sks=b&skv=2021-08-06&sig=XtSdw5k5pURiT9lqzBN37Cm5Vo2ZQE8fbAx4qkL%2BKzs%3D"
            u = urlopen(image_url)
            raw_data = u.read()
            u.close()

            photo = ImageTk.PhotoImage(data=raw_data)
            
            label = customtkinter.CTkLabel(image=photo, master=frame_right, text="")
            label.image = photo
            label.grid(column=0,row=0)

        # Left Frame

        def generate_photo():
            prompt_text = ai_gen_photo.photo_prompt
            response = openai.Image.create(
            prompt=prompt_text,
            n=1,
            size="512x512"
        )
            image_url = response['data'][0]['url']
            ai_gen_photo.photo_url = image_url
            print(prompt_text)
            print(image_url)
            
            u = urlopen(image_url)

            raw_data = u.read()

            u.close()

            photo = ImageTk.PhotoImage(data=raw_data)
            label = customtkinter.CTkLabel(image=photo, master=frame_right, text="")
            label.image = photo
            label.grid(column=0,row=0)
            

        # Generate AI generated image button
        generate_image_button = customtkinter.CTkButton(frame_left, text="Generate Image", command=generate_photo)
        generate_image_button.grid(column=0,row=0, padx=10,pady=10)
        
        # Write Prompt button
        # Method to open prompt window
        def open_prompt_window():
            if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
                self.toplevel_window = prompt_window()  # create window if its None or destroyed
            else:
                self.toplevel_window.focus()


        write_prompt_button = customtkinter.CTkButton(frame_left, text="Write Prompt", command=open_prompt_window)
        write_prompt_button.grid(column=0,row=1, padx=10,pady=10)
        write_prompt_button.grid(column=0,row=1, padx=10,pady=10)

            
        # Method to generate image (test)
       
 



        



app = App()
app.mainloop()