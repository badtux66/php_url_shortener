pipeline {
    agent any
    options {
        timestamps()
    }
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
                git branch: 'master', url: 'https://github.com/badtux66/php_url_shortener.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'cd polr && composer install --no-dev -o'
            }
        }
        stage('Copy .env') {
            steps {
                sh 'cd polr && cp .env.example .env'
            }
        }
        stage('Set APP_KEY') {
            steps {
                sh 'cd polr && php artisan key:generate'
            }
        }
        stage('Configure Polr') {
            steps {
                sh 'cd polr && php artisan polr:configure'
            }
        }
        stage('Deploy to Target') {
            steps {
                sshagent(['ssh-agent']) {
                    sh "sshpass -p '${SSH_PASSWORD}' scp -o StrictHostKeyChecking=no -r polr ${SSH_USER}@${TARGET_HOST}:~/"
                }
                sshagent(['ssh-agent']) {
                    sh "sshpass -p '${SSH_PASSWORD}' ssh -o StrictHostKeyChecking=no ${SSH_USER}@${TARGET_HOST} 'cd polr && composer install --no-dev -o && cp .env.example .env && php artisan key:generate && php artisan polr:configure'"
                }
            }
        }
    }
}
