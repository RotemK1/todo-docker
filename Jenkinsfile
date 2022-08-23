pipeline {
    agent any
    options {
        timestamps()
        timeout(time:10, unit:'MINUTES')
        
        buildDiscarder (logRotator(
            numToKeepStr: '4',
            daysToKeepStr: '7',
            artifactNumToKeepStr: '30'))
    }
    environment {

            DOCKER_IMAGE_AWS = "644435390668.dkr.ecr.us-east-1.amazonaws.com/rotem-todo-app"
            LOGIN_ECR= "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-east-1.amazonaws.com"
    }

    stages {
            // stage("BUILD APP + UNIT TEST"){
            //     when { expression { env.GIT_BRANCH != 'feature' }}
            //     steps{
            //         script{
            //             // withCredentials([usernamePassword(credentialsId: 'git_https_account', passwordVariable: 'password', usernameVariable: 'username')]) {
            //             //     git url: 'https://github.com/RotemK1/todo-docker.git'
            //                     //app_todo = docker.build('rotem-todo-app')
            //                     sh "docker-compose up --build -d"
            //                     sh "timeout 60 wget --retry-connrefused --tries=60 --waitretry=2 -q app_container:5000 -O /dev/null"
            //         }
            //     }
            // }
        

        // stage('E2E'){
        //     when { expression { env.GIT_BRANCH == 'feature' }}
        //     steps{
        //         echo "#########################################"
        //         echo "                 E2E                     "
        //         echo "#########################################"
        //         script{
        //                 sh "docker-compose up -d"

        //                 // TO DO TESTING WITH POST, GET, DELETE.

        //         }
        //     }
        // }


        stage('TAG & PUBLISH '){
            when { expression { env.GIT_BRANCH == 'master' }}
            steps{
                echo "#########################################"
                echo "           TAGGING AND PUBLISH          "
                echo "#########################################"

                script{
                    withCredentials([[
                        $class: 'AmazonWebServicesCredentialsBinding',
                        credentialsId: "aws_account",
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    ]]) {
                        //sh "aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.us-east-1.amazonaws.com"
                        NEW_TAG = sh(script: "aws ecr list-images --repository-name rotem-todo-app --filter --region us-east-1 tagStatus=TAGGED | grep imageTag | awk ' { print \$2 } ' |sort -V | tail -1 | sed 's/\"//g' |tr \".\" \" \" | awk ' { print \$1 \".\" \$2 \".\" \$3+1 } '", returnStdout: true).trim()
                        docker.withRegistry("https://644435390668.dkr.ecr.us-east-1.amazonaws.com/rotem-todo-app", "ecr:us-east-1:aws_account"){
                            app_todo = docker.build('rotem-todo-app')
                            if (NEW_TAG.isEmpty()){
                                app_todo.push("1.0.0")

                            }else{
                                app_todo.push("${NEW_TAG}")
                            }
                        }
                    }

                    withCredentials([usernamePassword(credentialsId: 'git_https_account', passwordVariable: 'password', usernameVariable: 'username')]) {
                                sh "git tag ${NEW_TAG}"
                                sh "git push https://${username}:${password}@github.com/RotemK1/todo-docker.git --tag"
                    }        
                }
            }
        }

        stage("Deploy"){
            
            when { expression { env.GIT_BRANCH == 'master' }}
            steps{
                script{
                    withCredentials([usernamePassword(credentialsId: 'git_https_account', passwordVariable: 'password', usernameVariable: 'username')]) {
                        //git url: 'https://github.com/RotemK1/app-helm.git'
                        sh  """ #!/bin/bash
                                mkdir helm-git && cd helm-git
                                git submodule add  https://${username}:${password}@github.com/RotemK1/app-helm.git app-helm
                                ls -laF
                                cd app-helm
                                git config --global user.email "rotem.devops.test@gmail.com"
                                git config --global user.name "Jenkins"
                                echo flaskapp.image.tag: "${NEW_TAG}" > ./flask-app/new_tag.yaml
                                git tag ${NEW_TAG}
                                git add .
                                git commit -am "added new version: ${NEW_TAG}"
                                git push https://${username}:${password}@github.com/RotemK1/app-helm.git --follow-tags
                            """
                    }
                } 
            } 
        }
    }

    post {
        always {
            sh "docker-compose down"
        }
    //     emailext (
    //         to:      "rotem.devops.test@gmail.com",
    //         subject: "Jenkins - ${env.JOB_NAME}, build ${env.BUILD_DISPLAY_NAME} - ${currentBuild.currentResult}",
    //         body:    """
    //         <p>Jenkins job <a href='${env.JOB_URL}'>${env.JOB_NAME}</a> (<a href='${env.BUILD_URL}'>build ${env.BUILD_DISPLAY_NAME}</a>) has result <strong>${currentBuild.currentResult}</strong>!
    //         <br>You can view the <a href='${env.BUILD_URL}console'>console log here</a>.</p>
    //         <br><strong>terraform Workspaces list:</strong></p>
    //         ${TERRAFORM_WORKSPACE}</p>
    //         <br><strong>Deleted Workspace list:</strong></p>
    //         <br>${DELETED_WORKSPACE}</p>
    //         <p>Source code from commit: <a href='${env.GIT_URL}/commit/${env.GIT_COMMIT}'>${env.GIT_COMMIT}</a> (of branch <em>${env.GIT_BRANCH}</em>).</p>
    //         <p><img src='https://www.jenkins.io/images/logos/jenkins/jenkins.png' alt='jenkins logo' width='123' height='170'></p>
    //         """
    //     )
    // }
        failure {
            echo "i failed!"
        }              
        success {
            echo 'I succeeded!'
        }
    }
}
