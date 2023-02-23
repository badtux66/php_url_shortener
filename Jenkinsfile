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

        stage('Create polr directory') {
            steps {
                sh 'mkdir polr'
            }
        }

        stage('Download .env.example') {
            steps {
                sh '''
                    cd polr
                    curl -o .env.example https://raw.githubusercontent.com/badtux66/polr/master/.env.example
                '''
            }
        }

        stage('Clone repository') {
            steps {
                git 'https://github.com/badtux66/polr.git'
            }
        }

        stage('Init Composer') {
            steps {
                sh '''
                    cd polr
                    composer init --name=badtux66/polr --description="Polr is a quick, modern and open-source link shortener" --type=project --stability=dev --license=MIT
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    cd polr
                    composer install
                '''
            }
        }

        stage('Copy .env') {
            steps {
                sh '''
                    cd polr
                    cp ../.env.example .env
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
                sshPublisher(
                    continueOnError: false,
                    failOnError: true,
                    publishers: [
                        sshPublisherDesc(
                            configName: 'my-ssh-server',
                            verbose: true,
                            transfers: [
                                sshTransfer(
                                    sourceFiles: 'polr/**',
                                    remoteDirectory: '/var/www/html/polr'
                                )
                            ]
                        )
                    ]
                )
            }
        }
    }
}
