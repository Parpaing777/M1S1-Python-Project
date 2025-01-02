import tkinter as tk
from tkinter import messagebox,ttk
import subprocess

def show_main_menu():
    clear_window()
    tk.Button(root, text='Process Corpus', command=process_corpus).pack(pady=30)
    tk.Button(root, text='Search Engine', command=show_search_engine).pack(pady=30)
    tk.Button(root, text='Exit', command=root.quit).pack(pady=10, side='bottom')

def process_corpus():
    try:
        subprocess.run(['python', 'mainU.py'])
        messagebox.showinfo('Info', 'Corpus Processed Successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Error: {e}')

def show_search_engine():
    clear_window()
    tk.Label(root, text='Enter Search Query:').pack(pady=10)
    search_entry = tk.Entry(root, width=40)
    search_entry.pack(pady=5)

    tk.Label(root, text='Set limit:').pack(pady=10)
    limit_slider = tk.Scale(root, from_=1, to=100, orient='horizontal', length=300)
    limit_slider.set(10)
    limit_slider.pack(pady=5)

    def search():
        query = search_entry.get()
        limit = limit_slider.get()

        # Create new window for loading screen
        results_window = tk.Toplevel(root)
        results_window.title('Search Results')
        loading_label = tk.Label(results_window, text='Loading ...')
        loading_label.pack(pady=10)

        # Progress bar
        progress_bar = ttk.Progressbar(results_window, orient='horizontal', length=300)
        progress_bar.pack(pady=10)

        # Update window to show progress bar
        results_window.update()

        def progress_callback(current, total):
            progress = (current / total) * 100
            progress_bar['value'] = progress
            results_window.update_idletasks()

        
        from Corpus import MdCorpus as mdc
        corpus = mdc('load').PKLload('600MVTV')

        from searchEngine import SearchEngine as se
        search = se(corpus)
        results = search.search(query, progress_callback, limit)

        # clear the loading msg and prog bar
        loading_label.pack_forget()
        progress_bar.pack_forget()
        
        if len(results) == 0:
            messagebox.showinfo('Info', 'No Results Found')
            results_window.destroy()
        else:
            tree = ttk.Treeview(results_window, columns=('ID', 'Title', 'Synopsis', 'Cosine Similarity'), show='headings')
            tree.heading('ID', text='ID')
            tree.column('ID', width=50)
            tree.heading('Title', text='Title')
            tree.heading('Synopsis', text='Synopsis')
            tree.heading('Cosine Similarity', text='Cosine Similarity')

            for index, row in results.iterrows():
                tree.insert('', 'end', values=(row['ID'], row['Title'], row['Synopsis'], row['Cosine Similarity']))
    
            tree.pack(expand=True, fill='both')

    tk.Button(root, text='Search', command=search).pack(pady=10)
    tk.Button(root, text='Back', command=show_main_menu).pack(pady=10)


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title('Movie Database')
root.geometry('400x400')
show_main_menu()
root.mainloop()
    

