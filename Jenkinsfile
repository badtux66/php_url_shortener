pipeline {
    agent any
    environment {
        PATH = "/usr/local/bin:${env.PATH}"
    }
    tools {
        maven "maven"
        git "git"
        composer "composer"
    }
    stages {
        stage('Clone repository') {
            steps {
                sh 'git clone -b master https://github.com/badtux66/polr'
            }
        }
        stage('Install dependencies') {
            steps {
                dir('polr') {
                    sh 'composer install --no-dev'
                }
            }
        }
        stage('Build application') {
            steps {
                dir('polr') {
                    sh 'php artisan key:generate'
                    sh 'php artisan migrate --seed'
                    sh 'php artisan storage:link'
                }
            }
        }
        stage('Deploy application') {
            steps {
                sh 'cp -R polr/. /var/www/gshortener'
            }
        }
        stage('Run migrations') {
            steps {
                sh 'cd /var/www/gshortener'
                sh 'php artisan migrate'
            }
        }
    }
}
