Vue.component('renderless-tags-input', {
    props: ['value'],
    data() {
        return {
            newTag: '',
        };
    },
    methods: {
        addTag() {
            if (this.newTag.trim().length === 0 || this.value.includes(this.newTag.trim())) {
                return;
            }
            this.$emit('input', [...this.value, this.newTag.trim()]);
            this.newTag = '';
        },
        removeTag(tag) {
            this.$emit('input', this.value.filter(t => t !== tag));
        }
    },
    render() {
        return this.$scopedSlots.default({
            tags: this.value,
            addTag: this.addTag,
            removeTag: this.removeTag,
            inputAttrs: {
                value: this.newTag,
            },
            inputEvents: {
                input: (e) => {
                    this.newTag = e.target.value;
                },
                keydown: (e) => {
                    if (e.keyCode === 13) {
                        e.preventDefault();
                        this.addTag();
                    }
                }
            }
        });
    },
});

getDatetime = function (date) {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();
    const minute = date.getMinutes();
    return year + '/' + month + '/' + day + ' ' + hour + ':' + minute;
};

function sleep(a) {
    var dt1 = new Date().getTime();
    var dt2 = new Date().getTime();
    while (dt2 < dt1 + a) {
        dt2 = new Date().getTime();
    }
    return;
}

const vm = new Vue({
    delimiters: ['[[', ']]'],
    el: '#main-app',
    data: {
        mdChecked: false,
        notes: [],
        noteId: '',
        noteTitle: '',
        noteContent: '',
        searchQuery: '',
        sortMethod: '',
        selectedIndex: '',
        tags: []
    },
    methods: {
        getNotesAPI: function () {
            var _this = this;
            _this.loading = true;
            $.ajax({
                url: './api/notes/',
                type: 'GET',
                dataType: 'JSON',
                timeout: 30000
            })
                .done(function (response) {
                    _this.error = 0;
                    _this.loading = false;
                    response.forIn(function (key, value, index) {
                        const gottenNoteId = value.id;
                        let exists = false;
                        _this.notes.forIn(function (key1, value1, index1) {
                            const originalNoteId = value1.id;
                            if (gottenNoteId === originalNoteId) {
                                exists = true;
                            }
                            if (value1.deleted === true) {
                                _this.deleteNote(key1);
                            }
                        });
                        if (exists === false) {
                            _this.notes.push(value);
                        }
                    });
                    _this.saveNotes();
                })
                .fail(function (error) {
                    if (_this.error <= 5) {
                        _this.error++;
                        _this.getNotesAPI();
                    } else {
                        _this.error = true;
                        _this.loading = false;
                    }
                });
        },
        postNotesAPI: function () {
            var _this = this;
            _this.loading = true;
            $.ajax({
                url: './api/notes/',
                type: 'POST',
                contentType: 'application/JSON',
                dataType: 'JSON',
                timeout: 30000,
                data: JSON.stringify(this.notes),
            })
                .done(function (response) {
                    _this.error = 0;
                    _this.loading = false;
                    _this.result = response;
                    console.log(response);
                })
                .fail(function (error) {
                    if (_this.error <= 5) {
                        _this.error++;
                        // _this.getNotesAPI();
                    } else {
                        _this.error = true;
                        _this.loading = false;
                    }
                });
            sleep(100);
        },
        deleteNotesAPI: function () {
            var _this = this;
            _this.loading = true;
            $.ajax({
                url: './api/notes/' + this.noteId + '/',
                type: 'DELETE',
                dataType: 'JSON',
                timeout: 30000
            })
                .done(function (response) {
                    _this.error = 0;
                    _this.loading = false;
                })
                .fail(function (error) {
                    if (_this.error <= 5) {
                        _this.error++;
                    } else {
                        _this.error = true;
                        _this.loading = false;
                    }
                });
        },
        selectNote: function (id) {
            const index = indexWhere(this.notes, note => note.id === id);
            this.noteId = this.notes[index].id;
            this.noteTitle = this.notes[index].title;
            this.noteContent = this.notes[index].content;
            this.tags = this.notes[index].tags;
            this.selectedIndex = index;
        },
        editNote: function () {
            if ((this.noteId === '') & (this.noteTitle !== '')) {
                this.noteId = this.registerNote(this.noteTitle, this.noteContent);
            }
            this.notes.filter(note => note.id === this.noteId)[0].title = this.noteTitle;
            this.notes.filter(note => note.id === this.noteId)[0].content = this.noteContent;
            this.notes.filter(note => note.id === this.noteId)[0].updated_at = getDatetime(new Date());
            this.notes.filter(note => note.id === this.noteId)[0].tags = this.tags;
            this.notes.filter(note => note.id === this.noteId)[0].isMarkdown = this.mdChecked;
            this.saveNotes();
        },
        addNote: function () {
            this.noteId = '';
            this.noteTitle = '';
            this.noteContent = '';
            this.tags = [];
            document.getElementById('input-title').focus();
        },
        registerNote: function () {
            const noteId = (function () {
                function s4() {
                    return Math.floor((1 + Math.random()) * 0x10000)
                        .toString(16)
                        .substring(1);
                }

                return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
            })();
            this.notes.push({
                id: noteId,
                title: this.noteTitle,
                content: this.noteContent,
                created_at: getDatetime(new Date()),
                updated_at: getDatetime(new Date()),
                tags: this.tags
            });
            this.saveNotes();
            return noteId;
        },
        saveNotes: function () {
            localStorage.setItem('notes', JSON.stringify(this.notes));
        },
        deleteNote: function (index) {
            if (index === undefined) {
                if (this.selectedIndex !== '') {
                    this.notes.splice(this.selectedIndex, 1);
                    this.saveNotes();
                    this.selectedIndex = '';
                    this.addNote();
                }
            } else {
                this.notes.splice(index, 1);
                this.saveNotes();
            }
        },
        loadNotes: function () {
            this.notes = JSON.parse(localStorage.getItem('notes'));
            if (!this.notes) {
                this.notes = [];
            }
        },
        sortNotes: function () {
            switch (this.sortMethod) {
                case 'title_ascend':
                    this.notes.sort(function (a, b) {
                        if (a.title < b.title) return -1;
                        if (a.title > b.title) return 1;
                        return 0;
                    });
                    break;
                case 'title_descend':
                    this.notes.sort(function (a, b) {
                        if (a.title > b.title) return -1;
                        if (a.title < b.title) return 1;
                        return 0;
                    });
                    break;
                case 'created_at_ascend':
                    this.notes.sort(function (a, b) {
                        if (a.created_at < b.created_at) return -1;
                        if (a.created_at > b.created_at) return 1;
                        return 0;
                    });
                    break;
                case 'created_at_descend':
                    this.notes.sort(function (a, b) {
                        if (a.created_at > b.created_at) return -1;
                        if (a.created_at < b.created_at) return 1;
                        return 0;
                    });
                    break;
                case 'updated_at_ascend':
                    this.notes.sort(function (a, b) {
                        if (a.updated_at < b.updated_at) return -1;
                        if (a.updated_at > b.updated_at) return 1;
                        return 0;
                    });
                    break;
                case 'updated_at_descend':
                    this.notes.sort(function (a, b) {
                        if (a.updated_at > b.updated_at) return -1;
                        if (a.updated_at < b.updated_at) return 1;
                        return 0;
                    });
                    break;
                default:
            }
        },
        update: _.debounce(function (e) {
            this.noteContent = e.target.value;
        }, 300)
    },
    computed: {
        filteredNotes() {
            return this.notes.filter(note => {
                var hit = note.title.toLowerCase().indexOf(this.searchQuery.toLowerCase()) > -1;
                const query = this.searchQuery;
                note.tags.forIn(function (key, value, index) {
                    if (value.toLocaleLowerCase().indexOf(query.toLocaleLowerCase()) > -1) {
                        hit = true;
                    }
                });
                if (note.deleted === true) {
                    hit = false;
                }
                return hit;
            });
        },
        compiledMarkdown: function () {
            return marked(this.noteContent, {sanitize: true});
        }
    },
    created() {
        window.addEventListener('beforeunload', this.postNotesAPI);
    },
    mounted: function () {
        this.loadNotes();
        if (document.getElementsByTagName('body')[0].getAttribute('data') == 'True') {
            // sleep(500);
            // console.log(this.notes);
            // this.postNotesAPI(); このタイミングでpostするとcsrfが無い(実際はあるが)というエラー
            this.getNotesAPI();
        }
        document.getElementById('input-title').focus();
        document.getElementById('side-menu-checkbox').addEventListener('change', function (e) {
            if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                if (document.getElementById('side-menu-checkbox').checked === true) {
                    document.getElementById('nav-bar').style.display = 'flex';
                } else {
                    document.getElementById('nav-bar').style.display = 'block';
                }
            }
        }, false);

    }
});

const vmmd = new Vue({
    el: '#editor',
    data: {
        input: '# hello'
    },
    computed: {
        compiledMarkdown: function () {
            return marked(this.noteContent, {sanitize: true});
        }
    },
    methods: {
        update: _.debounce(function (e) {
            this.noteContent = e.target.value;
        }, 300)
    }
});

Object.defineProperty(Object.prototype, 'forIn', {
    value: function (fn, self) {
        self = self || this;

        Object.keys(this).forEach(function (key, index) {
            var value = this[key];

            fn.call(self, key, value, index);
        }, this);
    }
});

function indexWhere(array, conditionFn) {
  const item = array.find(conditionFn);
  return array.indexOf(item);
}

// スクロールを同期してもあまりうまく動かない
// var mdinput = $('.md-input');
// var simulator = $('.md-simulator');
//
// mdinput.scroll(function () {
//
//     simulator.scrollTop(mdinput.scrollTop());//縦スクロールを連動させる。
//     simulator.scrollLeft(mdinput.scrollLeft());//横スクロールを連動させる。
//
// });