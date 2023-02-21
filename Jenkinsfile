pipeline {
    agent any

    tools {
        maven 'maven'
        git 'git'
    }

    stages {
        stage('Clone repository') {
            steps {
                sh 'git clone -b master https://github.com/badtux66/polr'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'cd polr && composer install --no-dev'
            }
        }

        stage('Build application') {
            steps {
                sh 'cd polr && php artisan key:generate'
            }
        }

        stage('Deploy application') {
            steps {
                sh 'cp -r polr /var/www/gshortener'
            }
        }

        stage('Run migrations') {
            steps {
                sh 'cd /var/www/gshortener && php artisan migrate --force'
            }
        }
    }
}
