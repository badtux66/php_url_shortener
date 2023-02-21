@Library('jenkins-shared-library@main') _

pipeline {
    agent any

    tools {
        maven 'apache-maven-3.8.3'
        git 'git'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                sh 'mvn clean package'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
                sh 'mvn test'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
                sh 'mvn deploy'
            }
        }
    }
}

@CompileStatic
def myFunction() {
    // your function code here
}
