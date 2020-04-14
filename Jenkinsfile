pipeline {
    agent { label 'docker-python' }
    options {
        timestamps()
    }
    environment {
        PROJECT_NAME = "newdeal-python-flask-sample"
    }
    stages {
        stage("dependency") {
            steps {
                sh "pip install --user -r requirements.txt"
            }
        }

        stage("test") {
           steps {
               sh "echo pytest"
           }
        }

        stage("Sonar") {
            steps {
                withSonarQubeEnv(installationName: 'SonarQube', credentialsId: 'seungjoon-sonar') {
                    sh "sonar-scanner \
                      -Dsonar.projectKey=${PROJECT_NAME} "
                }
            }
        }
        
        stage("packaging") {
            steps {
                sh "python setup.py sdist bdist_wheel"
            }
        }
        
        stage("Deploy To Nexus") {
            steps {
                configFileProvider([configFile(fileId: 'sw_architecture_pypirc', targetLocation: '/home/jenkins/.pypirc')]) {
                    sh "twine upload ./dist/*"
                }
            }
        }
    }
}
