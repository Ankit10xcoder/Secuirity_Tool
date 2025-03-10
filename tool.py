try:
    import streamlit as st
    import os
    from cryptography.fernet import Fernet
except ModuleNotFoundError as e:
    print("Required modules are missing. Please install dependencies using: \n\n    pip install streamlit cryptography")
    raise e

# Generate or loadstreamlit run tool.py key
KEY_FILE = "secret.key"

def load_key():
    if os.path.exists(KEY_FILE):
        return open(KEY_FILE, "rb").read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.encrypt(data)

def decrypt_data(data, key):
    cipher = Fernet(key)
    return cipher.decrypt(data)

# Load encryption key
key = load_key()

if 'st' in globals():  # Ensure Streamlit is available
    st.title("Cryptography Tool: Encrypt & Decrypt Files and Text")
    option = st.selectbox("Choose an option", ["Encrypt", "Decrypt"])
    file = st.file_uploader("Upload a file", type=["txt", "png", "jpg", "mp4", "mp3", "wav", "avi", "mov"])
    text_input = st.text_area("Or enter text to encrypt/decrypt")
    
    if file is not None or text_input:
        
        if file:
            file_bytes = file.read()
            file_name = file.name
            
            if option == "Encrypt":
                encrypted_data = encrypt_data(file_bytes, key)
                # Create download button for encrypted file
                st.download_button(
                    label="Download Encrypted File",
                    data=encrypted_data,
                    file_name=f"encrypted_{file_name}",
                    mime="application/octet-stream"
                )
            
            elif option == "Decrypt":
                try:
                    decrypted_data = decrypt_data(file_bytes, key)
                    # Create download button for decrypted file
                    st.download_button(
                        label="Download Decrypted File",
                        data=decrypted_data,
                        file_name=f"decrypted_{file_name}",
                        mime="application/octet-stream"
                    )
                except Exception:
                    st.error("Decryption failed. Ensure you uploaded a correctly encrypted file.")
        
        if text_input:
            if option == "Encrypt":
                encrypted_text = encrypt_data(text_input.encode(), key).decode()
                st.text_area("Encrypted Text", encrypted_text)
                # Create download button for encrypted text
                st.download_button(
                    label="Download Encrypted Text",
                    data=encrypted_text,
                    file_name="encrypted_text.txt",
                    mime="text/plain"
                )
            elif option == "Decrypt":
                try:
                    decrypted_text = decrypt_data(text_input.encode(), key).decode()
                    st.text_area("Decrypted Text", decrypted_text)
                    # Create download button for decrypted text
                    st.download_button(
                        label="Download Decrypted Text",
                        data=decrypted_text,
                        file_name="decrypted_text.txt",
                        mime="text/plain"
                    )
                except Exception:
                    st.error("Decryption failed. Ensure you entered correctly encrypted text.")
else:
    print("Streamlit is not available. Please ensure it is installed and run this script in a Streamlit-supported environment.")

# streamlit run tool.py