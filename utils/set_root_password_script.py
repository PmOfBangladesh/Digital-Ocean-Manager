def set_root_password_script(password: str) -> str:
    """Returns a cloud-init bash script to set root password and enable SSH login."""
    # Escape single quotes so the password is safe inside a single-quoted shell string.
    safe_password = password.replace("'", "'\\''")
    return (
        '#!/bin/bash\n'
        f"printf 'root:%s\\n' '{safe_password}' | chpasswd\n"
        'sed -i "s/^#*PermitRootLogin.*/PermitRootLogin yes/" /etc/ssh/sshd_config\n'
        'sed -i "s/^#*PasswordAuthentication.*/PasswordAuthentication yes/" /etc/ssh/sshd_config\n'
        'systemctl restart sshd || service ssh restart\n'
    )
