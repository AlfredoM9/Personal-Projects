/********************************************************************************
** Form generated from reading UI file 'Nova.ui'
**
** Created by: Qt User Interface Compiler version 5.9.9
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_NOVA_H
#define UI_NOVA_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_NovaClass
{
public:
    QWidget *centralWidget;
    QLabel *label;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *NovaClass)
    {
        if (NovaClass->objectName().isEmpty())
            NovaClass->setObjectName(QStringLiteral("NovaClass"));
        NovaClass->resize(600, 400);
        centralWidget = new QWidget(NovaClass);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        label = new QLabel(centralWidget);
        label->setObjectName(QStringLiteral("label"));
        label->setGeometry(QRect(0, 0, 161, 51));
        label->setTextFormat(Qt::AutoText);
        label->setScaledContents(false);
        label->setWordWrap(false);
        NovaClass->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(NovaClass);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 600, 26));
        NovaClass->setMenuBar(menuBar);
        mainToolBar = new QToolBar(NovaClass);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        NovaClass->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(NovaClass);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        NovaClass->setStatusBar(statusBar);

        retranslateUi(NovaClass);

        QMetaObject::connectSlotsByName(NovaClass);
    } // setupUi

    void retranslateUi(QMainWindow *NovaClass)
    {
        NovaClass->setWindowTitle(QApplication::translate("NovaClass", "Nova", Q_NULLPTR));
        label->setText(QApplication::translate("NovaClass", "<html><head/><body><p><span style=\" font-size:14pt;\">Select the User</span></p></body></html>", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class NovaClass: public Ui_NovaClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_NOVA_H
