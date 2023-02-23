pipeline {
    agent any
    environment {
        SSH_USER = 'pusula'
        SSH_PASSWORD = 'pusula+2023'
        TARGET_HOST = '192.168.30.21'
    }
    options {
        timeout(time: 1, unit: 'HOURS')
    }
    stages {
        stage('Cleanup') {
            steps {
                sh 'rm -rf polr'
            }
        }

        stage('Clone repository') {
            steps {
                git 'https://github.com/badtux66/php_url_shortener.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    cd polr
                    curl -sS https://getcomposer.org/installer | php
                    php composer.phar install --no-dev -o
                '''
            }
        }

        stage('Copy .env') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'ssh-credentials', usernameVariable: 'SSH_USER', passwordVariable: 'SSH_PASSWORD')]) {
                    sh "scp -r -o StrictHostKeyChecking=no .env ${SSH_USER}@${TARGET_HOST}:/var/www/polr/"
                }
            }
        }

        stage('Set APP_KEY') {
            steps {
                sshagent(credentials: ['ssh-credentials']) {
                    sh "ssh -o StrictHostKeyChecking=no ${SSH_USER}@${TARGET_HOST} 'cd /var/www/polr && php artisan key:generate'"
                }
            }
        }

        stage('Configure Polr') {
            steps {
                sshagent(credentials: ['ssh-credentials']) {
                    sh "ssh -o StrictHostKeyChecking=no ${SSH_USER}@${TARGET_HOST} 'cd /var/www/polr && cp .env.production .env'"
                }
            }
        }

        stage('Deploy to Target') {
            steps {
                sshagent(credentials: ['ssh-credentials']) {
                    sh "ssh -o StrictHostKeyChecking=no ${SSH_USER}@${TARGET_HOST} 'cd /var/www/polr && php artisan migrate --force'"
                }
            }
        }
    }
}
