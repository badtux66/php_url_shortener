pipeline {
    agent any

    environment {
        SSH_USER = 'pusula'
        SSH_PASSWORD = 'pusula+2023'
        TARGET_HOST = '192.168.30.21'
    }

    stages {
        stage('Cleanup') {
            steps {
                sh 'rm -rf polr'
            }
        }

        stage('Clone repository') {
            steps {
                sh '''
                    git clone https://github.com/badtux66/polr.git polr
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    cd polr
                    composer update
                    composer config --no-plugins allow-plugins.kylekatarnls/update-helper true
                    composer install
                '''
            }
        }

        stage('Copy .env') {
            steps {
                sh '''
                    cd polr
                    mv .env.setup .env
                '''
            }
        }

        stage('Set APP_KEY') {
            steps {
                sh '''
                    cd polr
                    php artisan key:generate
                '''
            }
        }

        stage('Configure Polr') {
            steps {
                sh '''
                    cd polr
                    sed -i "s/DB_DATABASE=homestead/DB_DATABASE=polr/g" .env
                    sed -i "s/DB_USERNAME=homestead/DB_USERNAME=root/g" .env
                    sed -i "s/DB_PASSWORD=secret/DB_PASSWORD=pusula_shortener_pass/g" .env
                '''
            }
        }

        stage('Deploy to Target') {
            steps {
                sh '''
                    sshpass -p $SSH_PASSWORD ssh -o StrictHostKeyChecking=no $SSH_USER@$TARGET_HOST "sudo -S dnf remove -y php-common && sudo -S dnf install -y epel-release && sudo -S dnf install -y https://rpms.remirepo.net/enterprise/remi-release-9.rpm && sudo -S dnf module reset -y php && sudo -S dnf module enable -y php:remi-7.4 <<< $SSH_PASSWORD && sudo -S dnf clean all <<< $SSH_PASSWORD && sudo -S dnf update -y <<< $SSH_PASSWORD && sudo -S dnf install -y --skip-broken httpd php php-mysqlnd php-pecl-zip-1.19.2-6.el9.x86_64 mariadb-server zip unzip <<< $SSH_PASSWORD"
                    sshpass -p $SSH_PASSWORD scp -o StrictHostKeyChecking=no -r polr $SSH_USER@$TARGET_HOST:/var/www/html/
                    sshpass -p $SSH_PASSWORD ssh -o StrictHostKeyChecking=no $SSH_USER@$TARGET_HOST "sudo -S dnf update -y <<< $SSH_PASSWORD && sudo -S dnf clean all <<< $SSH_PASSWORD && sudo -S dnf module enable -y php:remi-7.4 <<< $SSH_PASSWORD && sudo -S dnf install -y --skip-broken httpd php php-mysqlnd php-pecl-zip-1.19.2-6.el9.x86_64 mariadb-server zip unzip <<< $SSH_PASSWORD && cd /var/www/html/polr && sudo -S composer install <<< $SSH_PASSWORD && sudo -S chown -R apache:apache /var/www/html/polr <<< $SSH_PASSWORD && sudo -S chmod -R 755 /var/www/html/polr <<< $SSH_PASSWORD"
                '''
            }
        }
    }
}
