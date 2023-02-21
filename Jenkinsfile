pipeline {
    agent any

    tools {
        maven 'maven'
        git 'git'
    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'master', url: 'https://github.com/badtux66/polr'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'cd polr && composer install --no-dev'
            }
        }

        stage('Build application') {
            steps {
                sh 'cd polr && php artisan key:generate && npm install && npm run dev'
            }
        }

        stage('Deploy application') {
            steps {
                sh 'rsync -avz --delete-after -e "ssh -i /var/lib/jenkins/.ssh/id_rsa" polr/ user@123.123.123.123:/var/www/html/polr'
            }
        }

        stage('Run migrations') {
            steps {
                sh 'ssh -i /var/lib/jenkins/.ssh/id_rsa user@123.123.123.123 "cd /var/www/html/polr && php artisan migrate"'
            }
        }
    }
}
