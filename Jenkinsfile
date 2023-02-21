pipeline {
    agent any

    tools {
        maven "maven"
        git "git"
        composer "composer"
    }

    stages {
        stage('Clone repository') {
            steps {
                sh "git clone -b master https://github.com/badtux66/polr"
            }
        }

        stage('Install dependencies') {
            steps {
                dir('polr') {
                    sh "composer install --no-dev"
                }
            }
        }

        stage('Build application') {
            steps {
                dir('polr') {
                    sh "./vendor/bin/phinx migrate"
                }
            }
        }

        stage('Deploy application') {
            steps {
                dir('polr') {
                    sh "rsync -avz . root@165.227.183.80:/var/www/gshortener"
                }
            }
        }

        stage('Run migrations') {
            steps {
                dir('polr') {
                    sh "./vendor/bin/phinx migrate"
                }
            }
        }
    }
}
