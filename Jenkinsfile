pipeline {
    agent any

    environment {
        SSH_USER = 'pusula'
        SSH_KEY = credentials('polr-deployment-pipeline')
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
                withCredentials([sshUserPrivateKey(credentialsId: 'polr-deployment-pipeline', keyFileVariable: 'SSH_KEY')]) {
                    sh '''
                        cd polr
                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY $SSH_USER@$TARGET_HOST "mkdir -p /var/www/html/polr"
                        scp -o StrictHostKeyChecking=no -i $SSH_KEY -r * $SSH_USER@$TARGET_HOST:/var/www/html/polr/
                    '''
                }
            }
        }
    }
}
