def set_root_password_script(password: str) -> str:
    """Returns a cloud-init bash script to set root password and enable SSH login."""
    return (
        '#!/bin/bash\n'
        f'echo "root:{password}" | chpasswd\n'
        'sed -i "s/^#*PermitRootLogin.*/PermitRootLogin yes/" /etc/ssh/sshd_config\n'
        'sed -i "s/^#*PasswordAuthentication.*/PasswordAuthentication yes/" /etc/ssh/sshd_config\n'
        'systemctl restart sshd || service ssh restart\n'
    )
