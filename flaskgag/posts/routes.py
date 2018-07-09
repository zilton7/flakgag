from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskgag import db
from flaskgag.models import Post, Vote
from flaskgag.posts.forms import PostForm
from flaskgag.users.utils import save_post_picture


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post_picture_file = save_post_picture(form.post_picture.data, form.title.data)
        post_image_file = url_for('static', filename='post_pics/' + post_picture_file )
        post = Post(title=form.title.data, post_image_file=post_image_file, content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!!!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, legend='Create Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    # Dummy comment
    comment_author = 'Sabaka'
    comment_content = 'Nu nezinau kazkokia xuinia, cia nui nx...'
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, comment_author=comment_author,
                           comment_content=comment_content)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form,
                           legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route('/vote/<int:post_id>/<int:user_id>')
@login_required
def upvote(post_id, user_id):
    vote = Vote.query.filter_by(post_id=post_id, user_id=user_id).first()
    if vote is not None:
        db.session.delete(vote)
        db.session.commit()
        add_vote_to_post(post_id)
        flash('Your vote removed', 'danger')
    else:
        vote = Vote(post_id=post_id, user_id=user_id)
        db.session.add(vote)
        db.session.commit()
        add_vote_to_post(post_id)
        flash('Your vote added', 'success')
    #return '', 204
    return redirect(url_for('main.home'))


def add_vote_to_post(post_id):
    vote_count = Vote.query.filter_by(post_id=post_id).count()
    post_filter = Post.query.filter_by(id=post_id).first()
    post_filter.votes = vote_count
    db.session.commit()


@posts.route('/vote/guest/')
def upvote_guest():
    flash("You must be logged in to vote.", 'info')
    return redirect(url_for('users.login'))
