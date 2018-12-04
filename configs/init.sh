#!/bin/bash

# Download z for autojump
git clone https://github.com/rupa/z ~/.config/z
echo "source ~/.config/z/z.sh" >> ~/.bashrc

# Download Vundle for vim
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
wget -O ~/.vimrc https://raw.githubusercontent.com/lujiaying/jiayinglu/master/configs/vimrc
# Then Launch vim and run :PluginInstall

source ~/.bashrc
