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
                sh 'cd polr && vendor/bin/phinx migrate -e development'
            }
        }
        stage('Deploy application') {
            steps {
                sh 'echo "Deployment step"'
            }
        }
    }
}
