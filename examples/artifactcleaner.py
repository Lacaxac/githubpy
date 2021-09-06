

import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from datetime import datetime

import githubpy
from githubpy import GitHubClient
    
    
def SizeStr(size):
    if size >= 1e12:
        return f"{size/(1024**4):.1f}T"
    if size >= 1e9:
        return f"{size/(1024**3):.1f}G"
    if size >= 1e6:
        return f"{size/(1024**2):.1f}M"
    if size >= 1e3:
        return f"{size/1024:.1f}K"
    return f"{size}"
    

class ArtifactWindow(object):
    def __init__(self, token, owner, geometry=(500, 100, 600, 600)):
        self._ghc = GitHubClient(token=token, usesession=True)
        self._owner = owner
        self._artifacts = []
    
        self._mainw = mainW = QMainWindow()
            
        menuBar = mainW.menuBar()
        
        tb = mainW.addToolBar("")
        self._fetchAction = fetchAction = tb.addAction(QtGui.QIcon("data/refresh+icon-1320183705440102854_64.png"), "Fetch")
        fetchAction.triggered.connect(self.fetch_artifacts)
        
        self._deleteAction = tb.addAction(QtGui.QIcon("data/icon+x+icon-1320183702540076171_64.png"), "Delete")
        self._deleteAction.triggered.connect(self.delete_artifacts)
    
    
        table = self._table = QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(0)
        
        checkHeader = QTableWidgetItem()
        table.setHorizontalHeaderItem(0, checkHeader)
        table.setColumnWidth(0, 50)
        
        repoHeader = QTableWidgetItem("Repo")
        table.setHorizontalHeaderItem(1, repoHeader)
        table.setColumnWidth(1, 250)
        
        artifactHeader = QTableWidgetItem("Artifact")
        table.setHorizontalHeaderItem(2, artifactHeader)
        table.setColumnWidth(2, 200)
        
        sizeHeader = QTableWidgetItem("Size")
        table.setHorizontalHeaderItem(3, sizeHeader)
        table.setColumnWidth(3, 75)
        
        expiresHeader = QTableWidgetItem("Expires")
        table.setHorizontalHeaderItem(4, expiresHeader)
        table.setColumnWidth(4, 150)
        
        mainW.setCentralWidget(self._table)
        
        mainW.setGeometry(*geometry)
        
    def fetch_artifacts(self):
        self._fetchAction.setEnabled(False)
        ghc = self._ghc
        table = self._table
        table.clearContents()
        table.setRowCount(0)
        index = 0
        totalSize = 0
        #t0 = datetime.now()
        for repo in GitHubClient.paginateGenerate(ghc.ReposListForAuthenticatedUser, type=None):
            
            try:
                artifacts = GitHubClient.paginate(ghc.ActionsListArtifactsForRepo, self._owner, repo.name, extractor=lambda data: data.artifacts)
            except githubpy.UnexpectedResult:
                continue
            
            
            for artifact in artifacts:
                if artifact.expired:
                    continue
                self._artifacts.append((repo.name, artifact))
                totalSize += artifact.size_in_bytes
                table.setRowCount(index+1)
                table.setCellWidget(index, 0, QCheckBox())
                table.setColumnWidth(0, 35)
                
                repoCell = QTableWidgetItem(repo.name)
                table.setItem(index, 1, repoCell)
                
                artifactCell = QTableWidgetItem(artifact.name)
                table.setItem(index, 2, artifactCell)
                sizeCell = QTableWidgetItem(SizeStr(artifact.size_in_bytes))
                table.setItem(index, 3, sizeCell)
                dateStr = artifact.expires_at.strftime("%m/%d/%y %I:%M%p")
                dateCell = QTableWidgetItem(dateStr)
                table.setItem(index, 4, dateCell)
                index += 1
            
        resetT = self._ghc.rateLimitReset.strftime("%I:%M%p")
        self._mainw.statusBar().showMessage(f"{self._ghc.rateLimitRemaining} remaining  reset:{resetT}  total={SizeStr(totalSize)}")
        
        
        
        #print(f"fetched in {datetime.now()-t0}")
        self._fetchAction.setEnabled(True)
                
        return
    
    def delete_artifacts(self):
        
        col = 0
        n = 0
        toDelete = []
        for row in range(self._table.rowCount()):
            w = self._table.cellWidget(row, col) 
            if w.isChecked():
                n += 1
                toDelete.append(self._artifacts[row])
        
        msgBox = QMessageBox(QMessageBox.Warning, "Delete", 
                             f"YOU ARE ABOUT TO DELETE {n} ARTIFACTS\nAre you sure?", 
                             QMessageBox.Ok | QMessageBox.Cancel)
        
        result = msgBox.exec()
        if result == QMessageBox.Cancel:
            return
        
        ghc = self._ghc
        isinstance(ghc, GitHubClient)
        for reponame, artifact in toDelete:
            result = ghc.ActionsDeleteArtifact(self._owner, reponame, artifact.id)
            assert(isinstance(result, githubpy.HttpResponse))
        
        return
    
    def show(self):
        self._mainw.show()
        


def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-o", "--owner")
    parser.add_argument("-t", "--token")
    
    options = parser.parse_args()
    
    app = QApplication(sys.argv)
    

    size = app.primaryScreen().size()
    
    w = size.width()//2
    h = size.height()//2
    
    geometry = ((size.width()-w)//2, (size.height()-h)//2,
                w, h)

    
    AW = ArtifactWindow(token=options.token, owner=options.owner, geometry=geometry)
    AW.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()