#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_Nova.h"

class Nova : public QMainWindow
{
    Q_OBJECT

public:
    Nova(QWidget *parent = Q_NULLPTR);

private:
    Ui::NovaClass ui;
    void createButton();
};
