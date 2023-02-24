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
                    sudo dnf update
                    sudo dnf install -y sshpass
                    sshpass -p $SSH_PASSWORD ssh -o StrictHostKeyChecking=no $SSH_USER@$TARGET_HOST "sudo dnf update && sudo dnf install apache2 php mysql-server php-mysql -y"
                    sshpass -p $SSH_PASSWORD scp -o StrictHostKeyChecking=no -r polr $SSH_USER@$TARGET_HOST:/var/www/html/
                    sshpass -p $SSH_PASSWORD ssh -o StrictHostKeyChecking=no $SSH_USER@$TARGET_HOST "cd /var/www/html/polr && sudo composer install && sudo chown -R www-data:www-data /var/www/html/polr && sudo chmod -R 755 /var/www/html/polr"
                '''
            }
        }
    }
}
