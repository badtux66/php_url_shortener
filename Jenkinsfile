pipeline {
    agent any

    environment {
        SSH_USER = 'root'
        SSH_PASSWORD = 'pusula+2023'
    }

    stages {
        stage('Clean Up') {
            steps {
                deleteDir()
            }
        }

        stage('Clone repository') {
            steps {
                sshagent(credentials: ['<your_ssh_credentials_id>']) {
                    sh "ssh ${SSH_USER}@192.168.30.21 'sudo su && cd /var/www && git clone https://github.com/cydrobolt/polr.git --depth=1 && chmod -R 755 polr && chown -R apache polr && chcon -R -t httpd_sys_rw_content_t polr/storage polr/.env'"
                }
            }
        }

        stage('Install dependencies') {
            steps {
                sshagent(credentials: ['<your_ssh_credentials_id>']) {
                    sh "ssh ${SSH_USER}@192.168.30.21 'cd /var/www/polr && curl -sS https://getcomposer.org/installer | php && php composer.phar install --no-dev -o'"
                }
            }
        }

        stage('Build application') {
            steps {
                sshagent(credentials: ['<your_ssh_credentials_id>']) {
                    sh "ssh ${SSH_USER}@192.168.30.21 'cd /var/www/polr && php artisan build'"
                }
            }
        }

        stage('Deploy application') {
            steps {
                sshagent(credentials: ['<your_ssh_credentials_id>']) {
                    sh "rsync -avz --exclude '.env' ./ ${SSH_USER}@192.168.30.21:/var/www/polr"
                    sh "ssh ${SSH_USER}@192.168.30.21 'cp /var/www/polr/.env.production /var/www/polr/.env'"
                }
            }
        }

        stage('Run migrations') {
            steps {
                sshagent(credentials: ['<your_ssh_credentials_id>']) {
                    sh "ssh ${SSH_USER}@192.168.30.21 'cd /var/www/polr && php artisan migrate --force'"
                }
            }
        }
    }
}
